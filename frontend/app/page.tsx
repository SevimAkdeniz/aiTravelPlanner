import Navbar from "@/components/layout/Navbar";
import HeroSection from "@/components/home/HeroSection";
import Footer from "@/components/layout/Footer";
import MainChoiceSection from "@/components/home/MainChoiceSection";

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />

      <main className="flex-1">
        <HeroSection />

        <MainChoiceSection />

      </main>

      <Footer />
    </div>
  );
}