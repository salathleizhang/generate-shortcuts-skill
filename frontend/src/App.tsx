import { FormEvent, useState } from "react";
import { generateShortcut, getDownloadUrl, type GenerateShortcutResponse } from "./api/shortcuts";

const examplePrompt =
  "Create a Shortcut that asks for my name and then shows a friendly greeting.";

function App() {
  const [prompt, setPrompt] = useState(examplePrompt);
  const [name, setName] = useState("Greeting Shortcut");
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
      const response = await generateShortcut({ prompt, name, target });
      setResult(response);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Failed to generate shortcut.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="shell">
      <section className="hero">
        <p className="eyebrow">AI Shortcuts Generator</p>
        <h1>Describe a Shortcut. Download a signed `.shortcut` file.</h1>
        <p className="lede">
          This local demo uses a Vite + React frontend and a FastAPI backend running on your Mac.
          The backend generates a basic Shortcut plist, signs it with macOS Shortcuts, and returns a
          downloadable file.
        </p>
      </section>

      <section className="panel">
        <form onSubmit={handleSubmit} className="form">
          <label>
            Shortcut name
            <input value={name} onChange={(event) => setName(event.target.value)} />
          </label>

          <label>
            Target
            <select value={target} onChange={(event) => setTarget(event.target.value as "macOS" | "iOS")}>
              <option value="macOS">macOS</option>
              <option value="iOS">iOS</option>
            </select>
          </label>

          <label>
            What should the Shortcut do?
            <textarea value={prompt} onChange={(event) => setPrompt(event.target.value)} rows={8} />
          </label>

          <button disabled={isLoading || !prompt.trim() || !name.trim()}>
            {isLoading ? "Generating..." : "Generate Shortcut"}
          </button>
        </form>

        <aside className="status-card">
          <h2>Demo pipeline</h2>
          <ol>
            <li>React sends the prompt to FastAPI.</li>
            <li>FastAPI builds a minimal Shortcut plist.</li>
            <li>The plist is validated and written to a temp folder.</li>
            <li>Your Mac signs it with `shortcuts sign`.</li>
          </ol>

          {error ? <p className="error">{error}</p> : null}

          {result ? (
            <div className="result">
              <p>{result.message}</p>
              <p className={result.signed ? "badge signed" : "badge unsigned"}>
                {result.signed ? "Signed by macOS" : "Unsigned fallback"}
              </p>
              <a href={getDownloadUrl(result.download_url)} download>
                Download `.shortcut`
              </a>
            </div>
          ) : null}
        </aside>
      </section>
    </main>
  );
}

export default App;
