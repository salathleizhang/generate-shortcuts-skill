import { FormEvent, useState } from "react";
import { generateShortcut, getDownloadUrl, type GenerateShortcutResponse } from "./api/shortcuts";

const examplePrompt =
  "Create a Shortcut that asks for my name and then shows a friendly greeting.";

function App() {
  const [prompt, setPrompt] = useState(examplePrompt);
  const [target, setTarget] = useState<"macOS" | "iOS">("macOS");
  const [result, setResult] = useState<GenerateShortcutResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setResult(null);
    setIsLoading(true);

    try {
      const response = await generateShortcut({ prompt, name: "", target });
      setResult(response);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Failed to generate shortcut.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-frame">
      <section className="workspace">
        <section className="headline">
          <p className="eyebrow">AI Shortcuts Generator</p>
          <h1>
            say what you need, <span>get a Shortcut</span>
          </h1>
        </section>

        <section className="stage" id="generator">
          <form onSubmit={handleSubmit} className="composer">
            <div className="search-row">
              <label className="prompt-field">
                <span className="visually-hidden">What should the Shortcut do?</span>
                <input
                  value={prompt}
                  onChange={(event) => setPrompt(event.target.value)}
                  placeholder="Ask for text, summarize it, save it, send it..."
                />
              </label>

              <label className="target-field">
                <span className="visually-hidden">Target</span>
                <select value={target} onChange={(event) => setTarget(event.target.value as "macOS" | "iOS")}>
                  <option value="macOS">macOS</option>
                  <option value="iOS">iOS</option>
                </select>
              </label>

              <button disabled={isLoading || !prompt.trim()}>
                {isLoading ? "Generating..." : "Generate Shortcut"}
              </button>
            </div>
          </form>

          <div className="flow-strip" aria-hidden="true">
            <span>prompt</span>
            <i />
            <span>plist</span>
            <i />
            <span>download</span>
          </div>
        </section>

        <section className="details">
          <article>
            <h2>plain-language input,</h2>
            <p>no JSON wrangling.</p>
          </article>
          <article>
            <h2>skill docs included,</h2>
            <p>better action choices.</p>
          </article>
          <article>
            <h2>local signing,</h2>
            <p>ready for Shortcuts.</p>
          </article>
        </section>

        <section className="output-panel" aria-live="polite">
          <div className="pipeline">
            <h2>demo pipeline</h2>
            <ol>
              <li>React sends the prompt to FastAPI.</li>
              <li>Gemini drafts requirements from the skill docs.</li>
              <li>Gemini generates Shortcut JSON.</li>
              <li>The plist is validated and written.</li>
              <li>Your Mac signs it with <code>shortcuts sign</code>.</li>
            </ol>
          </div>

          <div className="response">
            {error ? <p className="error">{error}</p> : null}

            {result ? (
              <div className="result">
                <p>{result.message}</p>
                <p className="generated-name">Generated name: {result.name}</p>
                <p className={result.signed ? "badge signed" : "badge unsigned"}>
                  {result.signed ? "Signed by macOS" : "Unsigned fallback"}
                </p>
                <a className="secondary-link" href={getDownloadUrl(result.requirements_url)} target="_blank">
                  View generated requirements
                </a>
                <a className="secondary-link" href={getDownloadUrl(result.context_url)} target="_blank">
                  View prompt context
                </a>
                <a href={getDownloadUrl(result.download_url)} download>
                  Download `.shortcut`
                </a>
              </div>
            ) : (
              <div className="waiting-state">
                <span />
                <p>Your generated Shortcut will land here.</p>
              </div>
            )}
          </div>
        </section>
      </section>
    </main>
  );
}

export default App;
