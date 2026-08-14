import AuthVisual from "@/components/auth/AuthVisual";
import RegisterForm from "@/components/auth/RegisterForm";

export default function RegisterPage() {
  return (
    <main className="flex min-h-screen">
      <AuthVisual />
      <RegisterForm />
    </main>
  );
}