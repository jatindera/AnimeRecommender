import { Anime } from "@/types/anime";

export default function AnimeCard({ anime }: { anime: Anime }) {
  return (
    <div className="card w-64 fade-in hover:shadow-2xl hover:-translate-y-1 transition-all">
      <img
        src={anime.image_url || "/placeholder.jpg"}
        alt={anime.title}
        className="w-full h-40 object-cover rounded-xl mb-3"
      />
      <h3 className="text-lg font-semibold mb-1">{anime.title}</h3>
      <p className="text-sm text-indigo-400 mb-2">
        <strong>Genre:</strong> {anime.genre}
      </p>
      <p className="text-sm text-[var(--color-muted)] leading-snug line-clamp-4">
        {anime.synopsis}
      </p>
    </div>
  );
}
