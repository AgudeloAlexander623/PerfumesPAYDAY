const steps = [
  { num: "1", title: "Regístrate", desc: "Crea tu cuenta e inicia sesión para tener tu propio carrito." },
  { num: "2", title: "Explora", desc: "Busca y filtra por marca, género y familia olfativa." },
  { num: "3", title: "Arma tu carrito", desc: "Elige presentaciones de 30, 50 o 100 ml." },
  { num: "4", title: "Simula tu compra", desc: "Guarda tu dirección, confirma y consulta tu historial de pedidos." },
]

export const HowItWorks = () => {
  return (
    <section id="como-funciona" className="py-16 px-6 max-w-6xl mx-auto text-center border-t border-stone-200/60">
      <h2 className="text-2xl sm:text-3xl font-bold text-stone-900 font-serif mb-12">
        Cómo funciona
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
        {steps.map((item, idx) => (
          <div key={idx} className="flex flex-col items-center">
            <div className="w-10 h-10 rounded-full bg-[#7A1E35] text-white flex items-center justify-center font-bold text-sm mb-4 shadow-sm">
              {item.num}
            </div>
            <h3 className="font-bold text-stone-900 mb-2">{item.title}</h3>
            <p className="text-xs sm:text-sm text-stone-600 leading-relaxed max-w-xs">
              {item.desc}
            </p>
          </div>
        ))}
      </div>
    </section>
  )
}