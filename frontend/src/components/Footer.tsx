import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-border bg-background py-4">
      <div className="container px-4">
        <div className="flex flex-col md:flex-row justify-between items-left text-sm text-muted-foreground">
          <div className="mb-2 md:mb-0">
            ChatPCP is not affiliated with Pop Culture Parenting.
          </div>
        </div>
      </div>
    </footer>
  );
};
