export const Navbar = () => {
  return (
    <nav className="w-full bg-[#FAF7F2] border-b border-stone-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className="text-xl font-bold tracking-tight text-[#7A1E35] font-serif">
            PerfumesPAYDAY
          </span>
        </div>
        <div className="hidden md:flex space-x-8 text-sm font-medium text-stone-600">
          <a href="#catalogo" className="hover:text-[#7A1E35] transition-colors">Catálogo</a>
          <a href="#como-funciona" className="hover:text-[#7A1E35] transition-colors">Cómo funciona</a>
          <a href="#mayoristas" className="hover:text-[#7A1E35] transition-colors">Mayoristas</a>
          <a href="#iniciar-sesion" className="hover:text-[#7A1E35] transition-colors">Iniciar sesión</a>
        </div>
        <button className="px-5 py-2.5 text-sm font-medium text-white bg-[#7A1E35] rounded-md hover:bg-[#63182b] transition-all shadow-sm">
          Registrarse
        </button>
      </div>
    </nav>
  )
}