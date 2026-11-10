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

    return(
     <div>
       <h1>NakamaLog</h1>
       <ul>
         {animes.map(Anime => (
           <li key={Anime.id}>
             {Anime.name} ({Anime.release_year})
             <button onClick={() => verReviews(Anime.id)}>Ver reviews</button>
           </li>
         ))}
       </ul>

       <h2>Reviews</h2>
       <ul>
         {reviews.map(r => <li key={r.id}>{r.rating}/10 - {r.comment}</li>)}
       </ul>
     </div>
   );
}
