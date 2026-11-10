export const Footer = () => {
  return (
    <>
      {/* Sección Mayoristas */}
      <section id="mayoristas" className="bg-[#7A1E35] text-white py-16 px-6 text-center mt-12">
        <h2 className="text-2xl sm:text-3xl font-bold font-serif mb-2">Ventas al por mayor</h2>
        <p className="text-stone-200 text-sm">Próximamente</p>
      </section>

      {/* Footer final */}
      <footer className="bg-[#FAF7F2] py-8 px-6 text-center border-t border-stone-200">
        <span className="font-serif font-bold text-[#7A1E35] text-sm">PerfumesPAYDAY</span>
        <p className="text-[11px] text-stone-500 mt-1">
          Proyecto académico. Simulador sin pagos, facturación ni envíos reales.
        </p>
      </footer>
    </>
  )
}