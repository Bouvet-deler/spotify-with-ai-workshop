import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import { Track } from "../model/Playlist";
import { Spinner } from "../components/Spinner/Spinner";
import styles from "./CoverGeneratorPage.module.css";

export const CoverGeneratorPage = () => {
  const { playlistId } = useParams<{ playlistId: string }>();
  const [tracks, setTracks] = useState<Track[]>([]);
  const [coverUrl, setCoverUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTracks = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`/api/get-tracks?playlist_id=${playlistId}`);
        setTracks(response.data);
        setError(null);
      } catch (err) {
        console.error("Error fetching tracks:", err);
        setError("Failed to load tracks. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    if (playlistId) {
      fetchTracks();
    }
  }, [playlistId]);

  const generateCover = async () => {
    try {
      setGenerating(true);
      setError(null);
      const response = await axios.get(`/api/generate-cover?playlist_id=${playlistId}`);
      setCoverUrl(response.data.image_url);
    } catch (err) {
      console.error("Error generating cover:", err);
      setError("Failed to generate cover. Please try again.");
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return <Spinner />;
  }

  if (error && !tracks.length) {
    return (
      <div className={styles.container}>
        <p style={{ color: "red" }}>{error}</p>
        <Link to="/">
          <button>Back to Playlists</button>
        </Link>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <Link to="/">
        <button className={styles.backButton}>← Back to Playlists</button>
      </Link>

      <h1>Generate Cover Image</h1>

      <div className={styles.tracksSection}>
        <h2>Tracks in Playlist ({tracks.length})</h2>
        <ul className={styles.trackList}>
          {tracks.slice(0, 10).map((item, index) => (
            <li key={index}>
              <strong>{item.track.name}</strong> by{" "}
              {item.track.artists.map((a) => a.name).join(", ")}
            </li>
          ))}
        </ul>
        {tracks.length > 10 && <p>...and {tracks.length - 10} more tracks</p>}
      </div>

      <button
        onClick={generateCover}
        disabled={generating || tracks.length === 0}
        className={styles.generateButton}
      >
        {generating ? "Generating..." : "Generate AI Cover Image"}
      </button>

      {generating && (
        <div className={styles.generatingSection}>
          <Spinner />
          <p>Creating your unique cover image...</p>
        </div>
      )}

      {error && coverUrl === null && (
        <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>
      )}

      {coverUrl && (
        <div className={styles.coverSection}>
          <h2>Generated Cover</h2>
          <img src={coverUrl} alt="Generated playlist cover" className={styles.coverImage} />
        </div>
      )}
    </div>
  );
};
