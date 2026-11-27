const features = [
  {
    title: "Procesamiento Veloz",
    description: "Analiza y parsea grandes volúmenes de texto con algoritmos optimizados de alta precisión.",
    icon: "⚡"
  },
  {
    title: "Estructuración Automática",
    description: "Organiza registros individuales sin esfuerzo en modelos de datos listos para consumir.",
    icon: "⚙️"
  },
  {
    title: "Seguridad y Confiabilidad",
    description: "Diseño robusto que garantiza la integridad y consistencia de toda tu información.",
    icon: "🛡️"
  }
]

export const Features = () => {
  return (
    <section id="features" className="py-20 px-6 max-w-7xl mx-auto">
      <div className="text-center mb-16">
        <h2 className="text-3xl font-bold text-white">Todo lo que necesitas para tus datos</h2>
        <p className="mt-3 text-slate-400">Herramientas diseñadas para optimizar tus flujos de trabajo.</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {features.map((item, idx) => (
          <div key={idx} className="p-8 rounded-2xl bg-slate-900/50 border border-slate-800/80 hover:border-slate-700 transition-all group">
            <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">{item.icon}</div>
            <h3 className="text-xl font-semibold text-white mb-2">{item.title}</h3>
            <p className="text-slate-400 text-sm leading-relaxed">{item.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}