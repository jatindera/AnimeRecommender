export async function fetchRecommendations(query: string) {
  const res = await fetch("http://localhost:8080/recommend", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: query,
      mode: "AGENT",
    }),
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Failed to fetch recommendations: ${errorText}`);
  }

  return res.json();
}
