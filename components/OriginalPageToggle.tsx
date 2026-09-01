import Image from "next/image";
import { ImageIcon } from "lucide-react";

export default function OriginalPageToggle({
  screenshot,
  title,
}: {
  screenshot: string;
  title: string;
}) {
  return (
    <details className="group mt-6 rounded-xl border border-ink-200 bg-white dark:border-ink-800 dark:bg-ink-900">
      <summary className="flex cursor-pointer list-none items-center gap-2 px-4 py-3 text-sm font-medium text-ink-500 [&::-webkit-details-marker]:hidden dark:text-ink-400">
        <ImageIcon size={15} />
        View the original guide page (original layout)
      </summary>
      <div className="border-t border-ink-100 p-4 dark:border-ink-800">
        <Image
          src={screenshot}
          alt={title}
          width={1400}
          height={788}
          className="h-auto w-full rounded-lg border border-ink-100 dark:border-ink-800"
        />
      </div>
    </details>
  );
}
