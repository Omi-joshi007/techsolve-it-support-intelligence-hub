const examples = [
  "How has ticket volume changed over time?",
  "Which support teams need the most attention?",
  "What are the main problem areas affecting customers?",
];
const q = document.getElementById('question'),
	counter = document.getElementById('counter'),
	ask = document.getElementById('ask'),
	answer = document.getElementById('answer'),
	chips = document.getElementById('chips');
examples.forEach((t) => {
	const b = document.createElement('button');
	b.className = 'chip';
	b.textContent = t;
	b.onclick = () => {
		q.value = t;
		update();
		q.focus();
	};
	chips.appendChild(b);
});
function update() {
	counter.textContent = `${q.value.length} / 500`;
}
q.addEventListener('input', update);
async function run() {
	const value = q.value.trim();
	if (!value) {
		answer.className = 'answer error';
		answer.textContent = 'Please enter a question first.';
		return;
	}
	ask.disabled = true;
	answer.className = 'answer empty loading';
	answer.innerHTML = '';
	try {
		const r = await fetch('/api/ask', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ question: value }),
		});
		const data = await r.json();
		if (!r.ok) throw new Error(data.detail || 'Unable to complete the analysis.');
		answer.className = 'answer';
		answer.innerHTML = marked.parse(data.answer);
	} catch (e) {
		answer.className = 'answer error';
		answer.textContent = e.message;
	} finally {
		ask.disabled = false;
	}
}
ask.addEventListener('click', run);
q.addEventListener('keydown', (e) => {
	if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') run();
});
