export const Hero = () => {
  return (
    <section className="pt-16 pb-20 px-6 text-center max-w-4xl mx-auto">
      <span className="text-xs font-semibold tracking-widest text-[#7A1E35] uppercase">
        Tienda online de perfumes
      </span>
      <h1 className="mt-4 text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-stone-900 font-serif leading-tight">
        Explora, elige y compra tu próxima fragancia
      </h1>
      <p className="mt-4 text-sm sm:text-base text-stone-600 max-w-2xl mx-auto">
        Regístrate, arma tu carrito, guarda tu dirección de envío y simula tu compra en una experiencia inspirada en MercadoLibre.
      </p>
      
      <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center items-center">
        <button className="px-6 py-3 font-medium text-white bg-[#7A1E35] rounded-md hover:bg-[#63182b] transition-all shadow-sm">
          Explorar catálogo
        </button>
        <button className="px-6 py-3 font-medium text-stone-800 bg-white border border-stone-300 rounded-md hover:bg-stone-50 transition-all">
          Crear cuenta
        </button>
      </div>
      <p className="mt-4 text-xs text-stone-400">
        Simulador académico: no cobra dinero real ni envía productos reales.
      </p>
    </section>
  )
}