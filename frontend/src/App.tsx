import { useEffect, useState } from "react"

interface Anime {
  id: number
  name: string
  release_year: number
}

interface Review {
  id: number
  rating: number
  comment: string
}

function TarjetaAnime({ anime, onVerReviews }: { anime: Anime; onVerReviews: (id: number) => void }) {
  return (
    <li className="card">
      <div className="card-info">
        <strong>{anime.name}</strong> ({anime.release_year})
      </div>
      <button onClick={() => onVerReviews(anime.id)}>Ver reviews</button>
    </li>
  )
}

function TarjetaReview({ review }: { review: Review }) {
  return (
    <li className="card">
      <span className="badge">{review.rating}/10</span>
      <p>{review.comment}</p>
    </li>
  )
}

export default function App() {
  const [animes, setAnimes] = useState<Anime[]>([])
  const [reviews, setReviews] = useState<Review[]>([])

  useEffect(() => {
    fetch('http://localhost:8000/animes')
       .then(response => response.json())
       .then(data => setAnimes(data));
  }, [])

  function verReviews(id: number) {
    fetch(`http://localhost:8000/animes/${id}/reviews`)
       .then(response => response.json())
       .then(data => setReviews(data));
  }

  return (
    <main className="layout">
      <header>
        <h1>NakamaLog</h1>
      </header>

      <div className="contenido">
        <section>
          <h2>Catálogo</h2>
          <ul>
            {animes.map(Anime => (
              <TarjetaAnime key={Anime.id} anime={Anime} onVerReviews={verReviews} />
            ))}
          </ul>
        </section>

        <section>
          <h2>Reviews</h2>
          <ul>
            {reviews.map(r => (
              <TarjetaReview key={r.id} review={r} />
            ))}
          </ul>
        </section>
      </div>
    </main>
  );
}
