import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Episode } from '../types';

interface EpisodeDetailsProps {
  episode: Episode;
  onBack: () => void;
}

export const EpisodeDetails: React.FC<EpisodeDetailsProps> = ({ episode, onBack }) => {
  return (
    <>
      <div className="sticky top-0 bg-background border-b border-border p-3 sm:p-4 flex items-center">
        <button 
          onClick={onBack}
          className="p-2 hover:bg-secondary rounded-lg transition-colors mr-2"
        >
          <svg className="w-5 h-5 text-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        <h2 className="text-lg sm:text-xl font-bold text-foreground truncate">{episode.title}</h2>
        <a 
          href={episode.link}
          target="_blank" 
          rel="noopener noreferrer"
          className="p-2 hover:bg-secondary rounded-lg transition-colors ml-2"
        >
          <svg className="w-5 h-5 text-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 18v-6a9 9 0 0 1 18 0v6" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z" />
          </svg>
        </a>
      </div>
      <div className="p-4 sm:p-6">
        <p className="text-base sm:text-lg text-muted-foreground mb-4 sm:mb-6">{episode.summary}</p>
        
        <div className="mt-4 sm:mt-6">
          <div className="space-y-3 sm:space-y-4">
            <div className="bg-secondary rounded-xl p-4 sm:p-5 border border-border">
              <div className="prose dark:prose-invert max-w-none text-sm sm:text-base">\
                <ReactMarkdown>{episode.cheat_sheet}</ReactMarkdown>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}; 
