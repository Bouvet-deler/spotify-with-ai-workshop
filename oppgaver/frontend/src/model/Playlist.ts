export interface Playlist {
  id: string;
  name: string;
}

export interface Track {
  track: {
    name: string;
    artists: { name: string }[];
  };
}
