"use client";

import { useState } from "react";

interface Props {
  onSearch: (query: string) => void;
}

export default function SearchBar({ onSearch }: Props) {
  const [query, setQuery] = useState("");

  return (
    <div className="flex justify-center items-center gap-3 mb-10">
      <input
        type="text"
        placeholder="Enter anime name or theme..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-72 sm:w-96 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-[var(--color-card)] text-[var(--color-text)] shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
      />
      <button
        onClick={() => onSearch(query)}
        className="btn-primary text-base"
      >
        Search
      </button>
    </div>
  );
}
