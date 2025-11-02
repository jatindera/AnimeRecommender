"use client";

import { useState } from "react";
import SearchBar from "./components/SearchBar";
import { fetchRecommendations } from "@/lib/api";

export default function Home() {
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSearch(query: string) {
    if (!query) return;
    setLoading(true);
    setError(null);
    setAnswer(null);

    try {
      const data = await fetchRecommendations(query);
      setAnswer(data.answer || "No answer received.");
    } catch (err) {
      console.error(err);
      setError("Failed to fetch recommendations.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12 text-center">
      <h2 className="anime-gradient text-4xl sm:text-5xl font-extrabold mb-8">
        Anime Recommender 🎥
      </h2>

      <SearchBar onSearch={handleSearch} />

      {loading && (
        <p className="text-indigo-400 text-lg mt-6 animate-pulse">
          Fetching recommendations...
        </p>
      )}
      {error && <p className="text-red-400 mt-4">{error}</p>}

      {answer && (
        <div className="bg-[var(--color-card)] text-left rounded-2xl p-6 mt-10 shadow-lg whitespace-pre-line leading-relaxed fade-in">
          <h3 className="text-xl font-semibold mb-3 text-[var(--color-accent)]">
            Recommendations:
          </h3>
          <div className="prose prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: formatMarkdown(answer) }} />
        </div>
      )}
    </div>
  );
}

/**
 * Convert simple markdown-style bold/italic to HTML for display.
 * This is a lightweight formatting helper.
 */
function formatMarkdown(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/\n/g, "<br/>");
}
