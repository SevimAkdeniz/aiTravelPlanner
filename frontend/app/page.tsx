import Navbar from "@/components/layout/Navbar";
import HeroSection from "@/components/home/HeroSection";
import Footer from "@/components/layout/Footer";

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />

      <main className="flex-1">
        <HeroSection />
      </main>

      <Footer />
    </div>
  );
}