import Link from "next/link";

export default function NotFound() {
  return (
    <div className="mx-auto flex max-w-lg flex-col items-center px-4 py-24 text-center">
      <h1 className="text-3xl font-bold text-ink-900 dark:text-white">404</h1>
      <p className="mt-2 text-ink-500 dark:text-ink-400">
        Cette page du guide n&apos;existe pas ou plus.
      </p>
      <Link
        href="/"
        className="mt-6 rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
      >
        Retour à l&apos;accueil
      </Link>
    </div>
  );
}
