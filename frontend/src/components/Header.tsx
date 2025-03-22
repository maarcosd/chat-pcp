import React from 'react';

interface HeaderProps {
  isDark: boolean;
  onToggleDarkMode: () => void;
}

export const Header: React.FC<HeaderProps> = ({ isDark, onToggleDarkMode }) => {
  return (
    <header className="bg-background border-b border-border relative overflow-hidden">
      {/* Faded background hero image */}
      <div 
        className="absolute inset-0 opacity-15 bg-cover bg-center bg-top bg-no-repeat"
        style={{ backgroundImage: 'url("/hero-image.jpeg")' }}
      />
      
      {/* Content */}
      <div className="px-4 sm:px-6 py-4 sm:py-8 relative">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 sm:gap-6">
          <div className="flex items-center justify-between sm:flex-1">
            <div className="flex items-center gap-4 sm:gap-6">
              <div className="w-16 h-16 sm:w-24 sm:h-24 rounded-full overflow-hidden border-2 border-border shadow-sm">
                <img 
                  src="/hero-image-small.jpeg" 
                  alt="Pop Culture Parenting" 
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="flex flex-col">
                <div className="flex items-center gap-3">
                  <h1 className="text-2xl sm:text-3xl font-bold text-foreground">
                    ChatPCP
                  </h1>
                  <button
                    onClick={onToggleDarkMode}
                    className="sm:hidden p-2 rounded-lg bg-secondary hover:bg-secondary/80 transition-colors"
                  >
                    {isDark ? (
                      <svg className="w-4 h-4 text-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                      </svg>
                    ) : (
                      <svg className="w-4 h-4 text-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                      </svg>
                    )}
                  </button>
                </div>
                <p className="text-sm sm:text-lg text-muted-foreground mt-1 sm:mt-2 max-w-2xl">
                  Your AI-powered companion for navigating the journey of parenthood with confidence and understanding.
                </p>
              </div>
            </div>
            <button
              onClick={onToggleDarkMode}
              className="hidden sm:block p-2 rounded-lg bg-secondary hover:bg-secondary/80 transition-colors"
            >
              {isDark ? (
                <svg className="w-5 h-5 text-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              ) : (
                <svg className="w-5 h-5 text-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}; 
