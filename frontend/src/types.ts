export interface Episode {
  title: string;
  summary: string;
  pub_date: string;
  link: string;
  audio_url: string;
  keywords: string[];
  cheat_sheet?: string;
}

export interface PaginationMetadata {
  currentPage: number;
  pageSize: number;
  totalEpisodes: number;
  totalPages: number;
}

export interface EpisodesResponse {
  episodes: Episode[];
  pagination: PaginationMetadata;
}
