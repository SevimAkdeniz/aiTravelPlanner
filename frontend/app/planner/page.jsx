import Link from "next/link";

export default function PlannerPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-6">
      <div className="max-w-lg text-center">
        <h1 className="text-4xl font-bold text-foreground">
          Seyahatimi Planla
        </h1>

        <p className="mt-4 text-muted">
          Seyahat planlama ekranı yakında burada olacak.
        </p>

        <Link
          href="/"
          className="
            mt-8
            inline-flex
            rounded-xl
            bg-primary
            px-6
            py-3
            font-semibold
            text-white
          "
        >
          Ana Sayfaya Dön
        </Link>
      </div>
    </main>
  );
}