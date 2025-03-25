import React, { useCallback, useRef, useState } from 'react';
import { useDebounce } from '../hooks/useDebounce';
import { Episode } from '../types';

interface EpisodesListProps {
  episodes: Episode[];
  onEpisodeSelect: (episode: Episode) => void;
  isLoading: boolean;
  isLoadingMore: boolean;
  hasMore: boolean;
  onLoadMore: () => void;
  searchQuery: string;
  onSearchQueryChange: (query: string) => void;
}

const EpisodeSkeleton = () => (
  <div className="p-3 sm:p-4 rounded-xl bg-secondary border border-border animate-pulse">
    <div className="h-4 bg-muted rounded w-3/4 mb-2"></div>
    <div className="h-3 bg-muted rounded w-full mb-2"></div>
    <div className="h-3 bg-muted rounded w-1/2 mb-2"></div>
    <div className="flex items-center justify-between mt-2">
      <div className="h-3 bg-muted rounded w-24"></div>
      <div className="h-3 bg-muted rounded w-16"></div>
    </div>
  </div>
);

export const EpisodesList: React.FC<EpisodesListProps> = ({ 
  episodes, 
  onEpisodeSelect, 
  isLoading,
  isLoadingMore,
  hasMore,
  onLoadMore,
  searchQuery,
  onSearchQueryChange
}) => {
  const [isSearchVisible, setIsSearchVisible] = useState(false);
  const [localSearchQuery, setLocalSearchQuery] = useState(searchQuery);
  const debouncedSearchQuery = useDebounce(localSearchQuery, 300);
  const observer = useRef<IntersectionObserver>();

  // Update local state when parent's search query changes
  React.useEffect(() => {
    setLocalSearchQuery(searchQuery);
  }, [searchQuery]);

  // Update parent's search query when debounced value changes
  React.useEffect(() => {
    if (debouncedSearchQuery !== searchQuery) {
      onSearchQueryChange(debouncedSearchQuery);
    }
  }, [debouncedSearchQuery, searchQuery, onSearchQueryChange]);

  const lastEpisodeRef = useCallback((node: HTMLDivElement) => {
    if (isLoadingMore) return;
    if (observer.current) observer.current.disconnect();

    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasMore) {
        onLoadMore();
      }
    });

    if (node) observer.current.observe(node);
  }, [isLoadingMore, hasMore, onLoadMore]);

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 sm:p-6 border-b border-border bg-background sticky top-0 z-10">
        <div className="flex items-center justify-between">
          <div className={`transition-all duration-300 ${isSearchVisible ? 'opacity-0 h-0 overflow-hidden' : 'opacity-100'}`}>
            <h2 className="text-lg sm:text-xl font-bold text-foreground">Episodes & Resources</h2>
            <p className="text-xs sm:text-sm text-muted-foreground">Browse through our collection of easily actionable advice for each episode.</p>
          </div>
          <div className={`transition-all duration-300 flex items-center gap-2 ${isSearchVisible ? 'w-full' : ''}`}>
            {isSearchVisible && (
              <input
                type="text"
                placeholder="Search episodes..."
                value={localSearchQuery}
                onChange={(e) => setLocalSearchQuery(e.target.value)}
                className="w-full px-3 py-2 text-sm rounded-lg border border-input bg-secondary text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                autoFocus
              />
            )}
            <button
              onClick={() => setIsSearchVisible(!isSearchVisible)}
              className="p-2 text-muted-foreground hover:text-foreground rounded-full hover:bg-secondary transition-colors flex-shrink-0"
              aria-label="Toggle search"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      <div className="p-3 sm:p-4 space-y-2 sm:space-y-3 overflow-y-auto flex-1">
        {isLoading ? (
          <div className="space-y-2 sm:space-y-3">
            <EpisodeSkeleton />
            <EpisodeSkeleton />
            <EpisodeSkeleton />
            <EpisodeSkeleton />
            <EpisodeSkeleton />
          </div>
        ) : (
          <>
            {episodes.map((episode, index) => (
              <div
                key={episode.title}
                ref={index === episodes.length - 1 ? lastEpisodeRef : undefined}
                className="p-3 sm:p-4 rounded-xl cursor-pointer transition-all duration-200 bg-secondary hover:bg-secondary/80 border border-border hover:shadow-sm"
                onClick={() => onEpisodeSelect(episode)}
              >
                <h3 className="font-semibold text-sm sm:text-base text-foreground">{episode.title}</h3>
                <p className="text-xs sm:text-sm text-muted-foreground mt-1 sm:mt-2 line-clamp-2">{episode.summary}</p>
                <div className="flex items-center justify-between mt-2">
                  <p className="text-xs text-muted-foreground flex items-center">
                    <svg className="w-3 h-3 sm:w-4 sm:h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {new Date(episode.pub_date).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </p>
                  <a 
                    href={episode.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-primary hover:underline flex items-center"
                    onClick={(e) => e.stopPropagation()}
                  >
                    <svg className="w-3 h-3 sm:w-4 sm:h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 18v-6a9 9 0 0 1 18 0v6" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z" />
                    </svg>
                    Listen
                  </a>
                </div>
              </div>
            ))}
            {isLoadingMore && (
              <div className="space-y-2 sm:space-y-3">
                <EpisodeSkeleton />
                <EpisodeSkeleton />
                <EpisodeSkeleton />
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}; 
