import { Link } from "react-router-dom";
import styles from "./Navbar.module.css";

export const Navbar = () => {
  return (
    <nav className={styles.navbar}>
      <Link to="/" className={styles.logo}>
        <h1>🎵 Spotify AI Workshop</h1>
      </Link>
    </nav>
  );
};
