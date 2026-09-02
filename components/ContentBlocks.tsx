import type { ContentBlock } from "@/lib/types";

export default function ContentBlocks({ blocks }: { blocks: ContentBlock[] }) {
  return (
    <div className="space-y-4">
      {blocks.map((block, i) => {
        if (block.type === "table") {
          return (
            <div
              key={i}
              className="overflow-x-auto rounded-lg border border-ink-200 dark:border-ink-800"
            >
              <table className="w-full min-w-[480px] border-collapse text-sm">
                {block.headers && (
                  <thead>
                    <tr className="bg-ink-50 dark:bg-ink-900/60">
                      {block.headers.map((h, j) => (
                        <th
                          key={j}
                          className="whitespace-nowrap border-b border-ink-200 px-3 py-2.5 text-left text-xs font-semibold uppercase tracking-wide text-ink-500 dark:border-ink-800 dark:text-ink-400"
                        >
                          {h || <span className="text-ink-300">&mdash;</span>}
                        </th>
                      ))}
                    </tr>
                  </thead>
                )}
                <tbody>
                  {block.rows.map((row, r) => (
                    <tr
                      key={r}
                      className="border-b border-ink-100 last:border-0 odd:bg-white even:bg-ink-50/50 dark:border-ink-800 dark:odd:bg-ink-900 dark:even:bg-ink-900/50"
                    >
                      {row.map((cell, c) => (
                        <td
                          key={c}
                          className="whitespace-nowrap px-3 py-2 tabular-nums text-ink-700 dark:text-ink-200"
                        >
                          {cell === "" ? (
                            <span className="text-ink-300 dark:text-ink-600">
                              &ndash;
                            </span>
                          ) : cell === "✓" ? (
                            <span className="text-brand-600 dark:text-brand-400">
                              ✓
                            </span>
                          ) : (
                            cell
                          )}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
        }

        const size = block.size;
        const className =
          size >= 14
            ? "text-base font-medium text-ink-800 dark:text-ink-100"
            : size >= 10
            ? "text-sm text-ink-600 dark:text-ink-300"
            : "text-xs text-ink-400 dark:text-ink-500";

        return (
          <p key={i} className={className}>
            {block.text}
          </p>
        );
      })}
    </div>
  );
}
