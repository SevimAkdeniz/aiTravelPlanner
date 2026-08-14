import AuthVisual from "@/components/auth/AuthVisual";
import LoginForm from "@/components/auth/LoginForm";

export default function LoginPage() {
  return (
    <main className="flex min-h-screen w-full overflow-hidden">
      <AuthVisual />
      <LoginForm />
    </main>
  );
}