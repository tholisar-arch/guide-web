import Link from "next/link";
import Image from "next/image";

export default function ThumbCard({
  href,
  title,
  image,
}: {
  href: string;
  title: string;
  image: string;
}) {
  return (
    <Link
      href={href}
      className="group overflow-hidden rounded-xl border border-ink-200 bg-white shadow-card transition hover:-translate-y-0.5 hover:border-brand-300 hover:shadow-md dark:border-ink-800 dark:bg-ink-900"
    >
      <div className="relative aspect-[16/9] overflow-hidden bg-ink-50 dark:bg-ink-800">
        <Image
          src={image}
          alt={title}
          fill
          sizes="(max-width:768px) 100vw, 33vw"
          className="object-cover object-top transition group-hover:scale-105"
        />
      </div>
      <div className="p-3">
        <span className="line-clamp-2 text-sm font-medium text-ink-800 group-hover:text-brand-700 dark:text-ink-100 dark:group-hover:text-brand-300">
          {title}
        </span>
      </div>
    </Link>
  );
}
