const form = document.querySelector('#prediction-form');
const result = document.querySelector('#result');
const errorBox = document.querySelector('#form-error');
const button = document.querySelector('#submit-button');

async function checkService() {
  const label = document.querySelector('#api-status');
  const dot = document.querySelector('#status-dot');
  try {
    const response = await fetch('/api/v1/health', { headers: { Accept: 'application/json' } });
    if (!response.ok) throw new Error('Service unavailable');
    label.textContent = 'Service online';
    dot.classList.add('online');
  } catch {
    label.textContent = 'Service unavailable';
  }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  errorBox.hidden = true;
  result.hidden = true;
  button.disabled = true;
  button.textContent = 'Checking pattern…';
  try {
    const response = await fetch('/api/v1/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        steps_deviation_7d_pct: Number(form.elements.steps.value),
        sleep_deviation_7d_pct: Number(form.elements.sleep.value),
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'The check could not be completed.');
    const unusual = data.anomaly_label === -1;
    document.querySelector('#result-title').textContent = unusual
      ? 'A pattern worth noticing'
      : 'No unusual pattern flagged';
    document.querySelector('#result-copy').textContent = unusual
      ? 'This combination differs from patterns learned by the research model. One result alone does not indicate a health issue.'
      : 'This combination is within patterns learned by the research model. A typical result does not rule out a health concern.';
    document.querySelector('#result-score').textContent = Number(data.anomaly_score).toFixed(4);
    result.hidden = false;
    result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.hidden = false;
  } finally {
    button.disabled = false;
    button.innerHTML = 'Explore this pattern <span aria-hidden="true">→</span>';
  }
});

checkService();

const askForm = document.querySelector('#ask-form');
askForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const error = document.querySelector('#ask-error');
  const output = document.querySelector('#ask-result');
  const askButton = document.querySelector('#ask-button');
  error.hidden = true;
  output.hidden = true;
  askButton.disabled = true;
  askButton.textContent = 'Searching sources…';
  try {
    const response = await fetch('/api/v1/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ question: askForm.elements.question.value }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'The question could not be answered.');
    document.querySelector('#answer-text').textContent = data.answer;
    const list = document.querySelector('#source-list');
    list.replaceChildren();
    for (const source of data.sources) {
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.href = source.url;
      link.target = '_blank';
      link.rel = 'noreferrer';
      link.textContent = `${source.title} — ${source.source}`;
      item.append(link);
      list.append(item);
    }
    document.querySelector('#answer-mode').textContent =
      data.generated_by === 'local_model'
        ? 'Answered with an optional local model and retrieved sources.'
        : 'Extracted from retrieved sources.';
    output.hidden = false;
  } catch (errorValue) {
    error.textContent = errorValue.message;
    error.hidden = false;
  } finally {
    askButton.disabled = false;
    askButton.innerHTML = 'Search reviewed sources <span aria-hidden="true">→</span>';
  }
});
