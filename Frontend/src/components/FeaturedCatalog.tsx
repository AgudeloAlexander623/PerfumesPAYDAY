const products = [1, 2, 3]

export const FeaturedCatalog = () => {
  return (
    <section id="catalogo" className="py-16 px-6 max-w-6xl mx-auto">
      <div className="text-center mb-10">
        <h2 className="text-2xl sm:text-3xl font-bold text-stone-900 font-serif">Catálogo destacado</h2>
        <p className="mt-1 text-xs sm:text-sm text-stone-500">Precios de referencia en pesos colombianos (COP)</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {products.map((_, idx) => (
          <div key={idx} className="bg-white rounded-lg border border-stone-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div className="h-64 bg-stone-200 flex items-center justify-center text-stone-400 text-sm">
              [IMAGEN DEL PRODUCTO]
            </div>
            <div className="p-4 bg-white border-t border-stone-100">
              <span className="text-[10px] tracking-wider uppercase text-stone-400 font-semibold">[MARCA]</span>
              <h3 className="font-medium text-stone-900 text-sm mt-0.5">[NOMBRE DEL PERFUME]</h3>
              <p className="text-xs font-semibold text-stone-800 mt-3">Desde [PRECIO] COP</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}