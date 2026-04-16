import { FormEvent, useState } from "react";
import { Show, SignInButton, SignUpButton, UserButton, useAuth } from "@clerk/react";
import { generateShortcut, getDownloadUrl, type GenerateShortcutResponse } from "./api/shortcuts";
import iconUrl from "./assets/icon.svg";

const examplePrompt =
  "Create a Shortcut that asks for my name and then shows a friendly greeting.";

function App() {
  const { getToken } = useAuth();
  const [prompt, setPrompt] = useState(examplePrompt);
  const [target, setTarget] = useState<"macOS" | "iOS">("macOS");
  const [isTargetOpen, setIsTargetOpen] = useState(false);
  const [result, setResult] = useState<GenerateShortcutResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setResult(null);
    setIsLoading(true);

    try {
      const token = await getToken();
      const response = await generateShortcut({ prompt, name: "", target }, token);
      setResult(response);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Failed to generate shortcut.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-frame">
      <nav className="nav-bar" aria-label="Primary">
        <a className="brand" href="/" aria-label="ShortcutAI home">
          <img className="brand-logo" src={iconUrl} alt="" aria-hidden="true" />
          <span>ShortcutAI</span>
        </a>

        <div className="nav-auth">
          <Show when="signed-out">
            <SignInButton mode="modal">
              <button className="auth-btn">Sign In</button>
            </SignInButton>
            <SignUpButton mode="modal">
              <button className="auth-btn auth-btn-primary">Sign Up</button>
            </SignUpButton>
          </Show>
          <Show when="signed-in">
            <UserButton />
          </Show>
        </div>
      </nav>

      <section className="workspace">
        <section className="headline">
          <h1>
            say what you need, <span>get a Shortcut</span>
          </h1>
          <p className="eyebrow">AI Shortcuts Generator</p>
        </section>

        <section className="stage" id="generator">
          <Show when="signed-out">
            <div className="sign-in-prompt">
              <p>Sign in to start generating Shortcuts</p>
              <SignInButton mode="modal">
                <button className="auth-btn auth-btn-primary auth-btn-large">Get Started</button>
              </SignInButton>
            </div>
          </Show>

          <Show when="signed-in">
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

                <div
                  className="target-field"
                  onBlur={(event) => {
                    if (!event.currentTarget.contains(event.relatedTarget)) {
                      setIsTargetOpen(false);
                    }
                  }}
                >
                  <button
                    type="button"
                    className="target-trigger"
                    aria-expanded={isTargetOpen}
                    aria-haspopup="listbox"
                    onClick={() => setIsTargetOpen((current) => !current)}
                  >
                    <span>{target}</span>
                    <span className="chevron" aria-hidden="true" />
                  </button>
                  {isTargetOpen ? (
                    <div className="target-menu" role="listbox" aria-label="Target">
                      {(["macOS", "iOS"] as const).map((option) => (
                        <button
                          type="button"
                          className={target === option ? "target-item active" : "target-item"}
                          key={option}
                          role="option"
                          aria-selected={target === option}
                          onClick={() => {
                            setTarget(option);
                            setIsTargetOpen(false);
                          }}
                        >
                          {option}
                        </button>
                      ))}
                    </div>
                  ) : null}
                </div>

                <button disabled={isLoading || !prompt.trim()}>
                  {isLoading ? "Generating..." : "Generate Shortcut"}
                </button>
              </div>
            </form>
          </Show>
        </section>

        {error || result ? (
          <section className="output-panel" aria-live="polite">
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
            ) : null}
          </div>
          </section>
        ) : null}
      </section>
    </main>
  );
}

export default App;
