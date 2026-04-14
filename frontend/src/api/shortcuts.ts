const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export type GenerateShortcutRequest = {
  prompt: string;
  name: string;
  target: "macOS" | "iOS";
};

export type GenerateShortcutResponse = {
  job_id: string;
  status: "ready";
  name: string;
  download_url: string;
  requirements_url: string;
  context_url: string;
  signed: boolean;
  message: string;
};

export async function generateShortcut(
  payload: GenerateShortcutRequest,
): Promise<GenerateShortcutResponse> {
  const response = await fetch(`${API_BASE_URL}/api/shortcuts/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const detail = await readErrorDetail(response);
    throw new Error(detail || `Request failed with status ${response.status}`);
  }

  return response.json();
}

export function getDownloadUrl(path: string): string {
  if (path.startsWith("http")) {
    return path;
  }

  return `${API_BASE_URL}${path}`;
}

async function readErrorDetail(response: Response): Promise<string> {
  const text = await response.text();
  if (!text) {
    return "";
  }

  try {
    const body = JSON.parse(text) as { detail?: unknown };
    if (typeof body.detail === "string") {
      return body.detail;
    }
  } catch {
    return text;
  }

  return text;
}
