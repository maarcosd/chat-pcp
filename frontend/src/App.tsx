import { Thread } from '@/components/assistant-ui/thread';
import axios from 'axios';
import { useCallback, useEffect, useState } from 'react';
import './App.css';
import { ChatRuntimeProvider } from './components/ChatRuntimeProvider';
import { EpisodeDetails } from './components/EpisodeDetails';
import { EpisodesList } from './components/EpisodesList';
import { Footer } from './components/Footer';
import { Header } from './components/Header';
import { logPageView } from './lib/analytics';
import { Episode, EpisodesResponse } from './types';

type Tab = 'chat' | 'episodes';

function App() {
  const [episodes, setEpisodes] = useState<Episode[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedEpisode, setSelectedEpisode] = useState<Episode | null>(null);
  const [isDark, setIsDark] = useState(() => 
    window.matchMedia('(prefers-color-scheme: dark)').matches
  );
  const [activeTab, setActiveTab] = useState<Tab>('chat');

  // Track page view when the app loads
  useEffect(() => {
    logPageView();
  }, []);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e: MediaQueryListEvent) => setIsDark(e.matches);
    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  const fetchEpisodes = useCallback(async (page: number) => {
    try {
      const response = await axios.get<EpisodesResponse>(`http://localhost:3000/api/episodes?page=${page}&pageSize=7`);
      const { episodes: newEpisodes, pagination } = response.data;

      if (page === 1) {
        setEpisodes(newEpisodes);
      } else {
        setEpisodes(prev => [...prev, ...newEpisodes]);
      }

      setCurrentPage(pagination.currentPage);
      setHasMore(pagination.currentPage < pagination.totalPages);
    } catch (error) {
      console.error('Error fetching episodes:', error);
    } finally {
      setIsLoading(false);
      setIsLoadingMore(false);
    }
  }, [setEpisodes, setCurrentPage, setHasMore, setIsLoading, setIsLoadingMore]);

  useEffect(() => {
    const abortController = new AbortController();

    const fetchData = async () => {
      try {
        const response = await axios.get<EpisodesResponse>(
          `http://localhost:3000/api/episodes?page=1&pageSize=7`,
          { signal: abortController.signal }
        );
        const { episodes: newEpisodes, pagination } = response.data;

        setEpisodes(newEpisodes);
        setCurrentPage(pagination.currentPage);
        setHasMore(pagination.currentPage < pagination.totalPages);
      } catch (error) {
        if (axios.isCancel(error)) {
          console.log('Request cancelled');
          return;
        }
        console.error('Error fetching episodes:', error);
      } finally {
        setIsLoading(false);
        setIsLoadingMore(false);
      }
    };

    fetchData();

    return () => {
      abortController.abort();
    };
  }, []); // Empty dependency array since we only want to fetch on mount

  const loadMore = useCallback(() => {
    if (!isLoadingMore && hasMore) {
      setIsLoadingMore(true);
      fetchEpisodes(currentPage + 1);
    }
  }, [currentPage, fetchEpisodes, hasMore, isLoadingMore]);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark);
  }, [isDark]);

  return (
    <ChatRuntimeProvider>
      <div className="flex flex-col h-screen min-h-screen bg-background text-foreground">
        <Header isDark={isDark} onToggleDarkMode={() => setIsDark(!isDark)} />
        
        {/* Mobile Tab Navigation */}
        <div className="lg:hidden flex border-b border-border">
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex-1 py-3 px-4 text-sm font-medium ${
              activeTab === 'chat'
                ? 'text-primary border-b-2 border-primary'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            Chat
          </button>
          <button
            onClick={() => setActiveTab('episodes')}
            className={`flex-1 py-3 px-4 text-sm font-medium ${
              activeTab === 'episodes'
                ? 'text-primary border-b-2 border-primary'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            Episodes
          </button>
        </div>
        
        <div className="flex flex-col lg:flex-row flex-1 overflow-hidden">
          {/* Left Column - Chat Interface */}
          <div className={`relative flex flex-col w-full lg:w-1/2 bg-background border-b lg:border-b-0 lg:border-r border-border ${
            activeTab === 'chat' ? 'flex-1' : 'hidden lg:block'
          }`}>
            <div className="absolute inset-0">
              <Thread />
            </div>
          </div>

          {/* Right Column - Episodes List or Episode Details */}
          <div className={`w-full lg:w-1/2 bg-background overflow-y-auto ${
            activeTab === 'episodes' ? 'flex-1' : 'hidden lg:block'
          }`}>
            {!selectedEpisode ? (
              <EpisodesList 
                episodes={episodes} 
                onEpisodeSelect={setSelectedEpisode} 
                isLoading={isLoading}
                isLoadingMore={isLoadingMore}
                hasMore={hasMore}
                onLoadMore={loadMore}
              />
            ) : (
              <EpisodeDetails 
                episode={selectedEpisode} 
                onBack={() => setSelectedEpisode(null)} 
                isDark={isDark}
              />
            )}
          </div>
        </div>
        <Footer />
      </div>
    </ChatRuntimeProvider>
  );
}

export default App;
