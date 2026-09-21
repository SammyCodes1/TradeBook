type StallMarkProps = {
  className?: string;
};

export function StallMark({ className = "h-7 w-7" }: StallMarkProps) {
  return (
    <svg
      viewBox="0 0 32 32"
      className={className}
      aria-hidden="true"
      fill="currentColor"
    >
      <path d="M4.2 9.4C6.8 6.4 9.6 5 12.6 5c3 0 5.8 1.4 8.4 4.4C23.6 6.4 26.4 5 29.4 5c.3 0 .6.3.6.6v3.1c-2.5.1-4.8 1.3-6.9 3.6H9.9C7.8 10 5.5 8.8 3 8.7V5.6c0-.3.3-.6.6-.6 3 0 5.8 1.4 8.4 4.4Z" />
      <path d="M7 14.2h18v12.2a1.6 1.6 0 0 1-1.6 1.6H8.6A1.6 1.6 0 0 1 7 26.4V14.2Z" />
      <path d="M13 19.2h6v8.8h-6z" className="fill-ink" />
    </svg>
  );
}
