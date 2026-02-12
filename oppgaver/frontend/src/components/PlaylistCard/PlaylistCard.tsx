import { Playlist } from "../../model/Playlist";
import styles from "./PlaylistCard.module.css";

interface PlaylistCardProps {
  playlist: Playlist;
}

export const PlaylistCard = ({ playlist }: PlaylistCardProps) => {
  return (
    <div className={styles.card}>
      <h3>{playlist.name}</h3>
      {/* TODO: 1.2 */}
    </div>
  );
};
