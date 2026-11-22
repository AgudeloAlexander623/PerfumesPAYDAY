import { Navbar } from '../components/Navbar'
import { Hero } from '../components/Hero'
import { HowItWorks } from '../components/HowItWorks'
import { FeaturedCatalog } from '../components/FeaturedCatalog'
import { Footer } from '../components/Footer'

export const Home = () => {
  return (
    <div className="min-h-screen bg-[#FDFBF7] text-stone-800 font-sans">
      <Navbar />
      <main>
        <Hero />
        <HowItWorks />
        <FeaturedCatalog />
      </main>
      <Footer />
    </div>
  )
}