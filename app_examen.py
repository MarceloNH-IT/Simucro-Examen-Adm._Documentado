import json
import math
import os
import random
import threading
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 1. FUNCIÓN DE DISEÑO PERSONALIZADO
def aplicar_diseno_personalizado():
    st.markdown(
        """
        <style>
        /* 1. Fondo urbano con tu diseño personalizado de GitHub */
        .stApp {
            background-image: url("https://raw.githubusercontent.com/MarceloNH-IT/Examen_Adm_Consorcio_Final/main/Edificio_dise%C3%B1o.jpg");
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
        }

        /* 2. Contenedor central flotante para mantener la lectura perfecta */
        .block-container {
            background-color: #0D1117 !important;
            max-width: 820px !important;
            padding-top: 2.5rem !important;
            padding-bottom: 5rem !important;
            border-radius: 16px;
            box-shadow: 0px 0px 35px rgba(0, 0, 0, 0.95);
            border: 2px solid #30363d;
        }

        /* 3. Tamaño de letra (fácil lectura) */
        .stMarkdown, .stMarkdown p, .stMarkdown li,
        [data-testid="stMarkdownContainer"] {
            color: #F3F4F6 !important;
        }
        .stMarkdown p, p {
            font-size: 1.15rem !important;
            line-height: 1.65 !important;
        }
        h1, h2, h3 {
            color: #FFFFFF !important;
            line-height: 1.35 !important;
        }

        /* 4. Opciones de respuesta: círculos más grandes y más separadas */
        .stRadio label, .stRadio p, [data-testid="stWidgetLabel"] {
            color: #F9FAFB !important;
            font-size: 1.08rem !important;
            line-height: 1.55 !important;
        }
        .stRadio [data-testid="stMarkdownContainer"] p {
            margin-bottom: 0.25rem !important;
        }
        div[role="radiogroup"] {
            gap: 14px !important;
        }
        div[role="radiogroup"] > label {
            padding: 14px 16px !important;
            border-radius: 10px !important;
            background: rgba(255,255,255,0.06) !important;
            cursor: pointer;
            width: 100%;
        }
        div[role="radiogroup"] > label:hover {
            background: rgba(255,255,255,0.15) !important;
        }
        div[role="radiogroup"] > label > div:first-child {
            width: 30px !important;
            height: 30px !important;
            min-width: 30px !important;
            margin-right: 14px !important;
        }
        div[role="radiogroup"] > label > div:first-child > div {
            width: 14px !important;
            height: 14px !important;
        }
        div[data-testid="stRadio"] {
            margin-bottom: 28px;
        }

        /* Paneles, métricas y desplegables con fondo sólido */
        [data-testid="stMetric"],
        [data-testid="stExpander"],
        [data-testid="stAlert"] {
            background-color: #151B23 !important;
            border: 1px solid #30363D !important;
            border-radius: 10px !important;
        }

        /* Campos y botones */
        input, textarea, [data-baseweb="select"] > div {
            background-color: #151B23 !important;
            color: #FFFFFF !important;
        }
        .stButton button {
            font-weight: 700 !important;
            border-radius: 8px !important;
        }

        /* 5. Marquesina inferior / Footer */
        .footer-creador {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #000000;
            color: #ffffff;
            text-align: center;
            padding: 12px;
            font-weight: bold;
            font-size: 1.2rem;
            z-index: 99999;
            border-top: 4px solid #3b82f6;
            font-family: 'Courier New', Courier, monospace;
            box-shadow: 0px -5px 20px rgba(0,0,0,0.8);
        }

        .stApp > header {
            background-color: transparent !important;
        }
        </style>

        <div class="footer-creador">
            Creado con Python por Horacio Marcelo Nuñez
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------------------------
# FESTEJO: globos (30 s) + fuegos artificiales (10 s) + cartel que sube
# lentamente al medio, se queda 5 s y se esfuma.
# (st.markdown NO ejecuta JavaScript; por eso se usa un iframe que sí ejecuta
#  JS y dibuja sobre la página.)
# ---------------------------------------------------------------------------
_FESTEJO_HTML = """<!-- token __TOKEN__ -->
<script>
(function () {
  var P;
  try { P = window.parent; P.document.body; } catch (e) { return; }
  var doc = P.document;

  ['festejo-root', 'festejo-style', 'festejo-cartel'].forEach(function (id) {
    var v = doc.getElementById(id); if (v) v.remove();
  });

  var MENSAJE = __MENSAJE__;
  var FUEGOS = __FUEGOS__;
  var DURACION_GLOBOS = 30000;
  var DURACION_FUEGOS = 10000;

  var style = doc.createElement('style');
  style.id = 'festejo-style';
  style.textContent =
    '#festejo-root{position:fixed;inset:0;pointer-events:none;z-index:999998;overflow:hidden;}' +
    '.festejo-globo{position:absolute;bottom:-120px;line-height:1;will-change:transform;' +
      'animation-name:festejoSubir;animation-timing-function:linear;animation-fill-mode:forwards;}' +
    '@keyframes festejoSubir{' +
      '0%{transform:translate(0,0) rotate(-4deg);}' +
      '25%{transform:translate(18px,-30vh) rotate(4deg);}' +
      '50%{transform:translate(-18px,-65vh) rotate(-4deg);}' +
      '75%{transform:translate(18px,-100vh) rotate(4deg);}' +
      '100%{transform:translate(0,-135vh) rotate(-4deg);}}' +
    '#festejo-cartel{position:fixed;left:50%;top:50%;z-index:1000000;pointer-events:none;' +
      'padding:28px 44px;border-radius:22px;text-align:center;max-width:90vw;' +
      'font-family:"Source Sans Pro",Arial,sans-serif;font-size:clamp(26px,5vw,52px);font-weight:800;' +
      'color:#fff;background:linear-gradient(135deg,#16a34a,#22c55e);' +
      'border:4px solid #fff;box-shadow:0 10px 40px rgba(0,0,0,.5);' +
      'animation:festejoCartel 10.5s ease-in-out forwards;}' +
    '@keyframes festejoCartel{' +
      '0%{transform:translate(-50%,calc(-50% + 70vh));opacity:0;}' +
      '5%{opacity:1;}' +
      '38%{transform:translate(-50%,-50%);opacity:1;}' +
      '86%{transform:translate(-50%,-50%);opacity:1;}' +
      '100%{transform:translate(-50%,-50%) scale(1.08);opacity:0;}}';
  doc.head.appendChild(style);

  var root = doc.createElement('div');
  root.id = 'festejo-root';
  doc.body.appendChild(root);

  var cartel = doc.createElement('div');
  cartel.id = 'festejo-cartel';
  cartel.textContent = MENSAJE;
  doc.body.appendChild(cartel);
  setTimeout(function () { cartel.remove(); }, 10800);

  var colores = [0, 40, 120, 200, 280, 320];
  function nuevoGlobo() {
    var g = doc.createElement('div');
    g.className = 'festejo-globo';
    g.textContent = '\\uD83C\\uDF88';
    var size = 40 + Math.random() * 40;
    var dur = 9 + Math.random() * 5;
    g.style.left = (Math.random() * 96) + '%';
    g.style.fontSize = size + 'px';
    g.style.filter = 'hue-rotate(' + colores[Math.floor(Math.random() * colores.length)] + 'deg)';
    g.style.animationDuration = dur + 's';
    root.appendChild(g);
    setTimeout(function () { g.remove(); }, dur * 1000 + 200);
  }
  var t0 = Date.now();
  var timerGlobos = setInterval(function () {
    if (Date.now() - t0 >= DURACION_GLOBOS) { clearInterval(timerGlobos); return; }
    nuevoGlobo(); if (Math.random() > 0.4) nuevoGlobo();
  }, 450);

  function limpiar() {
    [root, style, cartel].forEach(function (e) { try { e.remove(); } catch (x) {} });
  }
  setTimeout(limpiar, DURACION_GLOBOS + 15000);
  // Si el usuario sale de la pantalla de resultados, se limpia todo
  if (window.addEventListener) {
    window.addEventListener('pagehide', limpiar);
    window.addEventListener('unload', limpiar);
  }

  function fuegos() {
    if (!P.confetti) return;
    var fin = Date.now() + DURACION_FUEGOS;
    var base = { startVelocity: 35, spread: 360, ticks: 60, zIndex: 999999 };
    var r = function (a, b) { return Math.random() * (b - a) + a; };
    var iv = setInterval(function () {
      var resta = fin - Date.now();
      if (resta <= 0) return clearInterval(iv);
      var n = 50 * (resta / DURACION_FUEGOS);
      P.confetti(Object.assign({}, base, { particleCount: n, origin: { x: r(0.1, 0.3), y: Math.random() - 0.2 } }));
      P.confetti(Object.assign({}, base, { particleCount: n, origin: { x: r(0.7, 0.9), y: Math.random() - 0.2 } }));
    }, 250);
  }
  if (FUEGOS) {
    if (P.confetti) { fuegos(); }
    else {
      var s = doc.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js';
      s.onload = fuegos;
      doc.head.appendChild(s);
    }
  }
})();
</script>
"""


def festejo_aprobado(token="0", mensaje="¡Felicitaciones, aprobaste! 🎉", fuegos=True):
    """Dibuja el festejo. Se llama en cada render de resultados mientras el
    contenido (token) sea el mismo, así no se reinicia ni se corta."""
    html = (_FESTEJO_HTML
            .replace("__TOKEN__", str(token))
            .replace("__MENSAJE__", json.dumps(mensaje))
            .replace("__FUEGOS__", "true" if fuegos else "false"))
    if hasattr(st, "iframe"):
        st.iframe(html, height=1)
    else:
        components.html(html, height=0)


# 2. CONFIGURACIÓN DE PÁGINA (DEBE SER EL PRIMER COMANDO DE STREAMLIT)
st.set_page_config(page_title="Simulacro RPA - Administrador de Consorcios", page_icon="🏢")

# 3. EJECUTAMOS LA FUNCIÓN DE DISEÑO
aplicar_diseno_personalizado()

DURACION = 120 * 60         # 120 minutos
APROBAR = 60                # % minimo (nota 6)
AREAS = {
    1: "Código Civil y Comercial",
    2: "Ley 941 de CABA y gestión del administrador",
    3: "Seguridad edilicia y AGC",
    4: "Relación laboral (CCT SUTERH)",
}
HIST = Path(os.environ.get("HISTORIAL_PATH", Path(__file__).with_name("historial.json")))

# Banco de preguntas: (área, pregunta, [opciones], índice_correcto, explicación)
Q = [
# ------------------------------------------------------------------ ÁREA 1: CCyC
(1, '¿En qué momento nace formalmente el consorcio de propietarios como persona jurídica independiente de sus miembros?', ['Al momento de terminarse la construcción física del edificio por parte de la empresa constructora.', 'Con la venta o escrituración de la primera unidad funcional a un tercero.', 'Con el otorgamiento de la escritura pública del Reglamento de Propiedad Horizontal y su inscripción registral.', 'Cuando se celebra la primera asamblea ordinaria y se elige al administrador matriculado.'], 2, 'El Art. 2044 del CCyC establece que el consorcio como persona jurídica nace con el otorgamiento del Reglamento de Propiedad Horizontal por escritura pública y su correspondiente inscripción registral.'),
(1, 'Según el Código Civil y Comercial, las estructuras de los balcones en un edificio de departamentos se consideran jurídicamente como:', ['Bienes de propiedad exclusiva y privada del dueño del departamento.', 'Bienes de propiedad común del consorcio.', 'Bienes mixtos, siendo la baranda común y el piso privado.', 'Bienes del dominio público de la Ciudad de Buenos Aires por dar a la vía pública.'], 1, 'Según el Art. 2041 inc. d) del CCyC, son partes necesariamente comunes los cimientos, columnas, vigas portantes, muros maestros y demás estructuras, incluso las de balcones, indispensables para mantener la seguridad. Los revestimientos superficiales y el uso del piso suelen quedar a cargo del propietario, pero la estructura es común.'),
(1, 'De acuerdo con el ordenamiento civil vigente, la designación de un Consejo de Propietarios en el edificio es:', ['Una obligación legal ineludible para todos los consorcios sin excepción.', 'Una facultad de la asamblea, la cual puede organizarlo y dotarlo de funciones si lo considera conveniente.', 'Obligatorio únicamente en aquellos edificios que superen las 20 unidades funcionales.', 'Un organo que solo se constituye de forma transitoria cuando el administrador renuncia o fallece.'], 1, 'El Art. 2064 del CCyC determina que la existencia del Consejo de Propietarios es una facultad atribuida a la asamblea, no una imposición legal obligatoria para todos los edificios.'),
(1, 'Para modificar las cláusulas del Reglamento de Propiedad Horizontal (que no afecten la propiedad exclusiva de una unidad), el Código Civil y Comercial exige de manera general una mayoría de:', ['Mayoría absoluta de los presentes en la asamblea.', 'Unanimidad absoluta de la totalidad de los propietarios del edificio.', 'Dos tercios (2/3) de la totalidad de los propietarios del consorcio.', 'Tres cuartas partes (3/4) de los propietarios que representen más de la mitad del valor del edificio.'], 2, 'Conforme al Art. 2057 del CCyC, la modificación del Reglamento de Propiedad Horizontal requiere de una resolución asamblearia adoptada por dos tercios de la totalidad de los propietarios.'),
(1, 'Cuando en una asamblea se adopta una decisión válida por la mayoría de los presentes, pero no se alcanza la mayoría de la totalidad de los propietarios, ¿qué plazo tienen los ausentes para oponerse antes de que la decisión quede firme?', ['Un plazo de 5 días hábiles desde que se les notifica fehacientemente la propuesta.', 'Un plazo de 15 días corridos desde la fecha de celebración de la asamblea.', 'Un plazo de 30 días desde que reciben la notificación de los acuerdos adoptados.', 'Carecen de derecho a oponerse si la asamblea cumplió con el quórum de inicio.'], 1, 'El Art. 2060 del CCyC prevé un plazo legal de 15 días corridos desde la notificación fehaciente de las propuestas de mayoría para que los propietarios ausentes puedan oponerse formalmente.'),
(1, 'Si un propietario del primer piso decide no utilizar el ascensor o la calefacción central del edificio, ¿puede eximirse total o parcialmente del pago de las expensas asignadas a esos servicios?', ['Sí, acreditando técnicamente que clausuró el radiador o el acceso a su unidad.', 'No, el Código establece que la renuncia al uso de partes o servicios comunes no libera al propietario del pago de las expensas ordinarias ni extraordinarias.', 'Sí, pero requiere la autorización firmada por el Consejo de Propietarios.', 'Solo si lo solicita judicialmente demostrando falta de capacidad económica.'], 1, 'El Art. 2049 del CCyC dispone expresamente que la renuncia al uso o goce de servicios o partes comunes no libera en ningún caso al propietario del pago de las expensas ordinarias ni extraordinarias.'),
(1, 'Si el Reglamento de Propiedad Horizontal no prevé una mayoría específica para remover al administrador, ¿con qué mayoría puede la asamblea decidir su cese si no existe una causa grave o delito?', ['Se requiere la unanimidad debido a que se interrumpe un contrato civil vigente.', 'Por mayoría absoluta (más de la mitad) de la totalidad de los propietarios del consorcio.', 'Por los dos tercios (2/3) de los propietarios presentes en la sesión.', 'El administrador no puede ser removido sin causa antes del vencimiento del plazo anual fijado por la Ley 941.'], 1, 'El Art. 2060 del CCyC establece que, a falta de previsión reglamentaria específica, las decisiones ordinarias como la remoción del administrador se adoptan por mayoría absoluta calculada sobre el total de propietarios. En CABA, el Art. 13 de la Ley 941 coincide: el administrador puede ser removido antes del vencimiento de su plazo por asamblea con la mayoría absoluta del Art. 2060.'),
(1, 'Según el Código Civil y Comercial de la Nación, ¿quién ejerce la representación legal del consorcio de propietarios frente a terceros?', ['El Consejo de Propietarios en forma colegiada.', 'El administrador.', 'El propietario que detente el mayor porcentaje de los co-dominios.', 'El presidente de la asamblea de propietarios.'], 1, 'El Art. 2065 del CCyC define que el administrador es el representante legal del consorcio de propietarios, con el carácter de mandatario.'),
(1, '¿Qué documento emitido y firmado por el administrador constituye título ejecutivo para iniciar el reclamo judicial de expensas atrasadas?', ['El libro de actas de la asamblea ordinaria.', 'El detalle de liquidación mensual enviado por correo electrónico.', 'El certificado de deuda de expensas.', 'El comprobante de pago de servicios comunes del edificio.'], 2, 'El Código Civil y Comercial instituye al certificado de deuda de expensas emitido por el administrador como el título ejecutivo hábil para promover el cobro rápido por vía judicial.'),
(1, '¿Cuál se considera el órgano deliberativo supremo de decisión dentro de la estructura de un consorcio de propiedad horizontal?', ['El administrador en ejercicio de sus facultades de superintendencia.', 'El Consejo de Propietarios reunido en sesión ordinaria.', 'La asamblea de propietarios.', 'La empresa administradora externa subcontratada.'], 2, 'La asamblea de propietarios constituye el órgano de gobierno y deliberación de máxima jerarquía institucional dentro del régimen legal de propiedad horizontal.'),
(1, '¿Quién asume jurídicamente el carácter de empleador del encargado y personal de maestranza afectado a un edificio de propiedad horizontal?', ['El administrador a título personal y con su patrimonio.', 'El Sindicato (SUTERH) en representación del gremio.', 'El consorcio de propietarios.', 'El Consejo de Propietarios en forma de junta directiva.'], 2, 'El consorcio de propietarios en su condición de persona jurídica independiente es el único y exclusivo titular de la relación laboral y carácter de empleador del personal de encargados.'),
(1, 'Si una unidad funcional se encuentra ocupada mediante un contrato de locación (alquiler), ¿quién es el sujeto obligado principal frente al consorcio por el pago de las expensas?', ['El locatario (inquilino) en forma directa y exclusiva.', 'La inmobiliaria que intervino en la rúbrica y administración del contrato de locación.', 'El propietario (locador) de la unidad funcional.', 'El garante solidario del contrato de alquiler.'], 2, 'El titular dominial registral (propietario/locador) es el sujeto obligado real (propter rem) frente al consorcio. Los pactos privados del contrato de alquiler no alteran el sujeto pasivo de la deuda ante el edificio.'),
(1, 'En caso de grave e inminente peligro de derrumbe o siniestro en una parte común, el administrador puede realizar reparaciones urgentes sin autorización previa de la asamblea. Esto constituye una facultad derivada de:', ['Sus obligaciones legales de conservación y custodia de los bienes comunes.', 'Una delegación expresa y permanente del Sindicato de Encargados.', 'Una autorización genérica extendida por la Comuna del barrio correspondiente.', 'No puede hacerlo bajo ninguna circunstancia sin convocar asamblea extraordinaria previa.'], 0, 'El administrador tiene entre sus deberes esenciales la conservación de las partes comunes y la adopción de medidas de seguridad urgentes frente a siniestros inminentes (Art. 2067 CCyC).'),
(1, 'Los sótanos, la vivienda del encargado, los pasillos de acceso a los departamentos y el hall de entrada del edificio son, según el ordenamiento legal:', ['Bienes susceptibles de apropiación o cerramiento privado por votación de los presentes.', 'Cosas y partes común de uso e interés común necesariamente inalienables.', 'Propiedad exclusiva de la empresa constructora hasta que se liquide el total de unidades.', 'Bienes comunales de libre usufructo por cualquier ciudadano de la vía pública.'], 1, 'El Art. 2041 del CCyC define estas locaciones comunes estructurales y de habitabilidad como partes indispensables y de carácter necesariamente común e inalienable del consorcio.'),
(1, '¿Qué porcentaje de votos de la totalidad de los propietarios se requiere para la realización de obras nuevos que beneficien a un solo propietario y no al consorcio general?', ['Mayoría simple de los presentes en la reunión.', 'Dos tercios de los propietarios de la totalidad del inmueble.', 'Unanimidad de la totalidad de los propietarios del consorcio.', 'No se permiten estas obras bajo el Código Civil y Comercial de la Nación.'], 2, 'El Art. 2052 del CCyC determina que si la mejora u obra nueva beneficia exclusivamente a un solo propietario, se requiere la unanimidad de votos de la totalidad de los propietarios.'),
(1, 'El Reglamento de Propiedad Horizontal y Administración forma parte de:', ['Un contrato comercial rescindible de forma unilateral por el administrador entrante.', 'El título de propiedad e integra el estatuto regulador del consorcio de carácter obligatorio.', 'Una ordenanza del Gobierno de la Ciudad Autónoma de Buenos Aires.', 'Un compendio de sugerencias operativas de uso optativo por la asamblea.'], 1, 'El reglamento constituye la norma estatutaria interna que rige con fuerza obligatoria sobre la totalidad de los integrantes del consorcio desde su inscripción registral en el dominio.'),
(1, 'Ante la renuncia o fallecimiento repentino del administrador, ¿quién asume transitoriamente la gestión de las tareas urgentes del consorcio según el Código Civil y Comercial?', ['El encargado del edificio de forma automática y obligatoria.', 'El Consejo de Propietarios, debiendo convocar a asamblea dentro de los plazos reglamentarios.', 'El propietario del departamento número uno (1).', 'El inspector general que asigne la Mesa de Entradas de la AGC de forma provisoria.'], 1, 'Ante vacancia, acefalía o impedimento del administrador, el Art. 2064 del CCyC faculta al Consejo de Propietarios para asumir las tareas administrativas urgentes y convocar a asamblea inmediata para designar reemplazo.'),
(1, 'La obligación "propter rem" en el régimen de propiedad horizontal implica que la deuda por expensas comunes acumulada por una unidad:', ['Sigue a la persona del deudor original y se extingue si el departamento se vende.', 'Viaja y se transmite junto con la cosa (unidad funcional), obligando al nuevo adquirente.', 'Se extingue de forma automática por el transcurso de seis meses corridos.', 'Debe ser absorbida de forma solidaria por el encargado y el administrador del edificio.'], 1, 'La obligación por expensas reviste carácter real (propter rem), lo cual significa que viaja indisolublemente ligada al dominio de la cosa, obligando solidariamente al adquirente posterior.'),
(1, '¿Cuál es el quórum general exigido para dar inicio válido a una asamblea ordinaria de propietarios si el reglamento no prevé una cláusula especial?', ['La presencia de la mitad más uno de la totalidad de los propietarios del consorcio.', 'El Código Civil y Comercial no establece un quórum rígido de apertura, permitiendo deliberar con los presentes y aplicar la propuesta de mayoría.', 'Un tercio exacto del porcentual inmobiliario total del edificio.', 'Obligatoriamente el 100% de los copropietarios del consorcio en primera convocatoria.'], 1, 'El Código moderno suprimió el régimen rígido de quórum, permitiendo sesionar de forma válida con los propietarios presentes y destrabar las decisiones mediante el procedimiento de notificación y propuesta de mayoría (Art. 2060).'),
(1, 'El administrador tiene la obligación civil de conservar y archivar los libros del consorcio. ¿Por cuánto tiempo mínimo debe resguardar la documentación respaldatoria de las cuentas de la gestión?', ['Por un período de dos años de forma improrrogable.', 'Por el término de diez años según las pautas generales de prescripción del Código Civil y Comercial.', 'Únicamente por el tiempo que dure su mandato anual según la Ley 941.', 'No existe plazo legal de conservación una vez aprobada la gestión en la asamblea anual.'], 1, 'El plazo de resguardo documental de comprobantes, facturas y libros contables contados a partir del cierre del ejercicio financiero se rige por la prescripción general de 10 años fijada por el orden civil.'),
# ------------------------------------------------------------------ ÁREA 2: Ley 941
(2, '¿Cuál es el organismo de la Ciudad Autónoma de Buenos Aires que actúa como autoridad de aplicación y control del Registro Público de Administradores (RPA)?', ['La Inspección General de Justicia (IGJ).', 'El Ministerio de Trabajo, Empleo y Seguridad Social de la Nación.', 'La Dirección General de Defensa y Protección al Consumidor.', 'La Agencia Gubernamental de Control (AGC).'], 2, 'La Dirección General de Defensa y Protección al Consumidor ejerce la fiscalización y poder de policía sobre la matrícula de administradores en el ámbito jurisdiccional de la Ciudad.'),
(2, '¿Cómo debe proceder obligatoriamente el administrador respecto a los fondos dinerarios que pertenecen al consorcio de propietarios en CABA?', ['Depositarlos en una cuenta bancaria a su nombre para agilizar transferencias operativas.', 'Mantenerlos en efectivo en una caja fuerte dentro de la oficina de la administración para urgencias.', 'Depositar los fondos en una cuenta bancaria abierta exclusivamente a nombre del consorcio.', 'Invertirlos temporalmente en instrumentos financieros particulares para generar honorarios extras.'], 2, 'La Ley 941 prohíbe taxativamente la confusión patrimonial, obligando a canalizar todos los ingresos y egresos ordinarios o extraordinarios por medio de cuenta bancaria exclusiva del consorcio.'),
(2, 'Conforme a la Ley 941 de CABA, ¿con qué periodicidad debe realizarse el curso de capacitación anual obligatorio para mantener vigente la matrícula en el RPA?', ['Cada cinco años con motivo de la recertificación de antecedentes de reincidencia.', 'Cada año.', 'Cada seis meses coincidiendo con las rendiciones semestrales ante el consorcio.', 'No requiere capacitación anual una vez aprobado el examen inicial de ingreso.'], 1, 'Para mantener la regularidad y validez de la matrícula activa en el RPA, se exige la aprobación periódica y anual de un trayecto de capacitación de actualización profesional en la materia.'),
(2, 'Según la normativa del Registro Público de Administradores (Ley 941), ¿cuál de las siguientes condiciones inhabilita de manera absoluta para inscribirse y matricularse?', ['Poseer título universitario de grado en una carrera ajena a las ciencias jurídicas o económicas.', 'Estar inhabilitado legalmente para ejercer el comercio.', 'Ser propietario de una unidad funcional dentro del radio de la Ciudad de Buenos Aires.', 'Tener domicilio fiscal constituido en la Provincia de Buenos Aires.'], 1, 'Estar inhabilitado legalmente para el ejercicio de actividades comerciales constituye un impedimento y exclusión absoluta para la inscripción o permanencia en los registros del RPA.'),
(2, '¿Cuál es el plazo de duración del mandato del administrador fijado por la Ley 941?', ['Un período de tres años de forma improrrogable.', 'Un plazo de un año (12 meses), a cuyo vencimiento debe someterse a renovación en asamblea.', 'El mandato es de carácter indefinido hasta tanto un propietario presente una impugnación formal.', 'El plazo que fije la antigüedad del encargado del edificio de forma solidaria.'], 1, 'El Art. 13 de la Ley 941 fija un plazo de un año para el ejercicio de la función del administrador, que puede ser renovado, obligándolo a rendir cuentas y someterse al voto de la asamblea de propietarios.'),
(2, 'El modelo único de liquidación de expensas establecido por las disposiciones de la Ley 941 ("Mis Expensas") exige de manera obligatoria incluir:', ['El listado de nombres, números de DNI y estado de salud de todos los residentes del edificio.', 'El detalle pormenorizado de ingresos, egresos, estado financiero de las cuentas bancarias y deudas de las unidades de forma transparente.', 'Copia certificada del título analítico del administrador del consorcio.', 'Una estimación aproximada del valor inmobiliario comercial en el mercado de cada departamento.'], 1, 'El esquema obligatorio unificado "Mis Expensas" resguarda el derecho constitucional a la información transparente, exigiendo el desglose pormenorizado de saldos, deudas, cuentas y proveedores del edificio.'),
(2, '¿Qué sanción máxima puede aplicar la Dirección General de Defensa y Protección al Consumidor a un administrador que ejerce la actividad de forma clandestina sin estar inscripto en el RPA?', ['Amonestación verbal privada sin registro en los legajos oficiales.', 'Multas cuantiosas calculadas en base a salarios de encargados, y la exclusión o imposibilidad de matricularse.', 'Arresto preventivo en dependencias policiales de la Ciudad Autónoma de Buenos Aires.', 'Expropiación de las oficinas comerciales de la empresa administradora a favor del consorcio afectado.'], 1, 'El ejercicio clandestino o marginal de la administración de consorcios en CABA es sancionado con severas multas punitivas de carácter pecuniario y la inhabilitación para matricularse formalmente en el registro.'),
(2, 'Para acreditar la vigencia de su matrícula ante los propietarios, el administrador tiene la obligación legal de exhibir en cada asamblea ordinaria:', ['Su certificado de inscripción y renovación emitido por el RPA de la CABA actualizado.', 'El balance fiscal consolidado de su propia empresa o monotributo del año comercial previo.', 'Una carta de recomendación de los miembros paritarios de la entidad gremial SUTERH.', 'La constancia de aprobación de sus exámenes de educación secundaria o universitaria.'], 0, 'Es un deber del administrador exhibir de forma transparente ante la asamblea ordinaria la credencial o certificado vigente de matriculación expedido por las autoridades del RPA de la Ciudad.'),
(2, 'Los denominados "administradores voluntarios o a título gratuito" (propietarios que administran su propio edificio y residen en él) según la Ley 941:', ['Están totalmente eximidos de inscribirse en el Registro Público de Administradores (RPA).', 'Deben inscribirse obligatoriamente en el RPA, pero bajo un régimen simplificado con menores requisitos formales.', 'Deben cumplir exactamente con las mismas exigencias y cursos de 60 horas que los administradores profesionales onerosos.', 'Tienen prohibido administrar si el consorcio supera las cinco unidades funcionales en total.'], 1, 'Los administradores voluntarios (copropietarios que ejercen ad honorem en su propio edificio) no están eximidos del registro; deben inscribirse obligatoriamente bajo un régimen simplificado adaptado.'),
(2, '¿Qué destino legal específico debe darse a los intereses recaudados por el administrador debido al pago fuera de término de las expensas por parte de copropietarios morosos?', ['Ingresan al patrimonio neto y exclusivo del consorcio de propietarios.', 'Corresponden al administrador en concepto de honorarios extraordinarios por gestiones de cobranza.', 'Se destinan a un fondo común administrado de forma directa por el Sindicato (SUTERH).', 'Deben ser girados de forma trimestral a las arcas del Tesoro del Gobierno de la Ciudad de Buenos Aires.'], 0, 'Los intereses punitorios o compensatorios percibidos por deudas en mora integran de forma directa el patrimonio contable del consorcio administrado, estando prohibido su desvío a honorarios del administrador.'),
(2, 'En la liquidación de expensas, las indemnizaciones por despido del encargado o las obras de remodelación estética integral del hall de entrada deben clasificarse legalmente como:', ['Expensas ordinarias habituales de liquidación directa al inquilino.', 'Expensas extraordinarias, debiendo ser asumidas exclusivamente por los propietarios de las unidades funcionales.', 'Gastos suntuarios no pasibles de cobro en la liquidación general del consorcio.', 'Aportes extraordinarios de recaudación directa en efectivo por fuera de la cuenta bancaria del consorcio.'], 1, 'Los gastos de carácter extraordinario, indemnizaciones de capital laboral estructural o mejoras estéticas de valorización patrimonial corresponden exclusivamente al propietario del inmueble (locador).'),
(2, 'Según el Código Civil y Comercial (Art. 2067 inc. j), ¿qué plazo tiene el administrador que cesa en sus funciones para entregar al consorcio o a quien lo reemplaza los libros, documentos y fondos?', ['Inmediatamente, en el acto mismo de la asamblea de remoción.', '15 días desde que cesa en sus funciones.', '30 días corridos, para permitir el cierre del balance por un contador.', 'No existe plazo: queda sujeto a lo que acuerden las partes.'], 1, 'El Art. 2067 inc. j) del CCyC fija un plazo de 15 días para entregar libros, documentos y fondos. La Ley 941 (Art. 9 inc. k) preveía 10 días para ponerlos a disposición, pero ese punto fue cuestionado por contradecir al Código de fondo y el TSJ de la CABA lo declaró inválido. Conviene conocer ambos plazos para el examen.'),
(2, 'La presentación de la Declaración Jurada (DDJJ) anual ante el Registro Público de Administradores (RPA) es una obligación que recae sobre:', ['El Consejo de Propietarios en representación de la comunidad vecinal.', 'Cada propietario de forma individual a través de la plataforma web de la Ciudad.', 'El administrador matriculado en ejercicio de su actividad profesional.', 'El encargado del edificio de forma solidaria con la empresa de limpieza contratada.'], 2, 'La presentación en término del informe contable, actas y actualización de datos a través de la Declaración Jurada anual ante el RPA es un deber personal e indelegable del administrador matriculado.'),
(2, 'Si un consorcio sufre perjuicios económicos debido a que el administrador no presentó las Declaraciones Juradas en término en el RPA, el administrador responde con:', ['Inmunidad civil por tratarse de un error administrativo involuntario o de fuerza mayor.', 'Su patrimonio personal frente a los daños y perjuicios ocasionados al consorcio administrado.', 'Una quita automática de 10% en los haberes jubilatorios futuros del encargado del edificio.', 'El consorcio no puede reclamar debido a que la responsabilidad frente al Estado es colectiva del edificio.'], 1, 'El administrador ejerce un mandato legal de fondos ajenos; la omisión dolosa o culposa de sus deberes administrativos formales lo hace responsable directo con su patrimonio personal ante perjuicios económicos al consorcio.'),
(2, '¿Qué porcentaje mínimo de asistencia o representación exige la ley para que la asamblea pueda sesionar de forma válida en segunda convocatoria si fracasa la primera por falta de quórum?', ['Un quórum estricto del 50% del valor inmobiliario total del edificio de forma obligatoria.', 'Se sesiona válidamente con los propietarios presentes, cuyas decisiones constituyen propuestas de mayoría a notificar a los ausentes.', 'Obligatoriamente dos tercios de la totalidad de las unidades funcionales del inmueble.', 'El examen técnico determina que la segunda convocatoria requiere la presencia física del Consejo de Propietarios en su totalidad.'], 1, 'El CCyC (Art. 2060) no prevé una "segunda convocatoria" automática como la vieja Ley 13.512: se delibera con los propietarios presentes y lo decidido se comunica de forma fehaciente a los ausentes, que tienen 15 días para oponerse.'),
(2, 'Conforme al artículo 15 de la Ley 941, ¿cuál de las siguientes conductas es considerada una infracción expresa a la normativa de administración?', ['Liquidar las expensas el quinto día del mes en lugar del primero.', 'No disponer de un fondo de reserva en dólares billete.', 'El incumplimiento de la obligación de verificar las pólizas de seguros obligatorias del consorcio.', 'Delegar las tareas de limpieza corriente del hall de entrada en una empresa externa contratada.'], 2, 'El artículo 15 sanciona taxativamente la omisión de contratar o mantener actualizados los seguros obligatorios de incendio, responsabilidad civil y los del personal contratado por el consorcio.'),
(2, '¿Con qué mayoría puede la asamblea renovar, o remover antes de su vencimiento, el mandato anual del administrador según el Art. 13 de la Ley 941?', ['Mayoría simple de los propietarios presentes.', 'Mayoría absoluta del Art. 2060 del CCyC (más de la mitad de la totalidad de los propietarios).', 'Unanimidad de la totalidad de los propietarios.', 'No se vota: la renovación es automática por el transcurso de los 12 meses.'], 1, 'El Art. 13 de la Ley 941 (texto según Ley 5.932) establece que el administrador es designado, renovado y removido por asamblea ordinaria o extraordinaria con la mayoría absoluta prevista en el Art. 2060 del CCyC, y que ejerce su función por el plazo de un año.'),
(2, '¿Cuál es el requisito indispensable respecto al Registro de Firmas de los copropietarios según las exigencias de la Ley 941 de la CABA?', ['El administrador debe llevar un registro actualizado de las firmas de los propietarios para cotejar la validez de los votos de las asambleas.', 'Las firmas deben ser certificadas de forma individual y obligatoria ante un escribano público nacional.', 'El registro de firmas debe ser remitido mensualmente en soporte de papel físico a la AGC.', 'No existe obligación de registrar firmas si el consorcio cuenta con un Consejo de Propietarios.'], 0, 'La Ley 941 impone el deber de llevar un Registro de Firmas de los copropietarios actualizado, que sirve de base formal para asegurar la legitimidad de las representaciones y votos en los actos asamblearios.'),
(2, 'De acuerdo al régimen de penalidades de la Ley 941, las reincidencias en infracciones a los deberes de administrador pueden acarrear además de las multas monetarias:', ['Una sanción accesoria de suspensión de la matrícula en el RPA por un plazo de hasta seis (6) meses.', 'La realización de trabajos comunitarios obligatorios en el barrio de la Comuna correspondiente.', 'El decomiso temporal de los bienes informáticos personales del administrador.', 'La inhabilitación perpetua sin derecho a réplica judicial.'], 0, 'La acumulación de infracciones o reincidencia faculta a Defensa del Consumidor a aplicar suspensiones temporales de la matrícula en el RPA de hasta 6 meses, o la exclusión definitiva según la gravedad.'),
(2, 'Cuando Defensa al Consumidor dicta una disposición sancionatoria firme contra un administrador, ¿en dónde debe ser publicada dicha resolución obligatoriamente?', ['En la cartelera del palacio de Tribunales de la Nación.', 'En el Boletín Oficial de la Ciudad Autónoma de Buenos Aires y en la web del registro.', 'En un diario de circulación nacional de forma anónima.', 'No se publica por razones de protección de datos personales del infractor.'], 1, 'Las sanciones aplicadas por el RPA que queden firmes en la vía administrativa se publican de forma obligatoria en el Boletín Oficial de la Ciudad para conocimiento público.'),
# ------------------------------------------------------------------ ÁREA 3: AGC / seguridad edilicia
(3, 'Bajo las competencias de la Agencia Gubernamental de Control (AGC) en CABA, ¿cuál de las siguientes instalaciones fijas requiere obligatoriamente inspección y certificación periódica por profesional habilitado?', ['El sistema de iluminación de emergencia individual de cada departamento privado.', 'El mantenimiento y conservación de ascensores, montacargas e instalaciones de elevación de uso común.', 'Los medidores de consumo eléctrico individuales de cada medidor interno.', 'El mobiliario de recepción en el hall de entrada del edificio.'], 1, 'Los medios técnicos de elevación mecánica común están sometidos al poder de policía directo de la AGC, requiriendo empresas conservadoras matriculadas y certificaciones mensuales obligatorias.'),
(3, 'En el marco de las tareas de control periódico edilicio en CABA, ¿con qué frecuencia obligatoria según las ordenanzas vigentes debe realizarse la limpieza y desinfección de los tanques de reserva de agua potable?', ['Una vez cada cinco años de forma improrrogable.', 'Una vez al mes en forma obligatoria.', 'Cada seis meses (semestralmente) incluyendo un análisis bacteriológico completo.', 'Exclusivamente cuando lo solicite un copropietario mediante nota formal ingresada por TAD.'], 2, 'Las reglamentaciones de ordenamiento sanitario e higiénico vigentes en CABA imponen la limpieza, vaciado preventivo, desinfección y análisis microbiológico de los tanques comunes de agua potable cada 6 meses.'),
(3, '¿Qué debe exhibir obligatoriamente el administrador de manera visible en el interior de la cabina de todo ascensor en funcionamiento en CABA?', ['Un cartel con el valor de las últimas expensas ordinarias aprobadas.', 'Un cartel con los datos identificatorios y número de habilitación de la empresa conservadora habilitada por la AGC.', 'El plano municipal de obra original del año de construcción del edificio.', 'Una copia del título profesional o analítico del administrador del consorcio.'], 1, 'Constituye una exigencia reglamentaria obligatoria e inspeccionable por la AGC mantener visible en la cabina del ascensor el cartel identificatorio técnico con los datos completos de la firma conservadora contratada.'),
(3, '¿Qué ley establece actualmente el marco general del Código de Edificación de la Ciudad Autónoma de Buenos Aires que rige los aspectos constructivos y de seguridad?', ['La Ley Nacional Nº 24.449 de Tránsito y Movilidad.', 'La Ley Nº 6.100 de la Ciudad Autónoma de Buenos Aires.', 'La Ley Nº 941 de Registro de Administradores de Consorcios.', 'La Ley Nº 13.512 de Propiedad Horizontal derogada en el orden civil.'], 1, 'La Ley N° 6.100 sancionada por la Legislatura aprueba e instrumenta el Código de Edificación moderno de la Ciudad de Buenos Aires aplicable a las estructuras e instalaciones de seguridad.'),
(3, '¿Qué normas técnicas de carácter nacional homologa el régimen de la Ciudad para regular de forma estricta el servicio de mantenimiento de las Instalaciones Fijas contra Incendios (IFCI)?', ['Normas IRAM (ej. IRAM 3546 y 3619) referidas a la evaluación y operatividad de sistemas de extinción.', 'Normas ISO 9001 exclusivamente referidas a procesos de administración de empresas comerciales.', 'Disposiciones internas del SUTERH sobre seguridad e higiene en el trabajo de los encargados.', 'Estándares de edificación e infraestructura de la Provincia de Córdoba.'], 0, 'El régimen de fiscalización edilicia local homologa técnicamente las Normas IRAM nacionales (como la 3546 y 3619) para auditar la calidad, presión operativa y vigencia de las instalaciones contra incendios (IFCI).'),
(3, 'Conforme a la normativa de fachadas y balcones en CABA, ¿cuál es la responsabilidad primordial del consorcio administrado en relación al frente del inmueble?', ['Pintar el frente del edificio obligatoriamente cada dos años sin excepción formal.', 'Garantizar la conservación y seguridad estructural de muros linderos, balcones y salientes para evitar desprendimientos.', 'Modificar la arquitectura exterior sin autorización municipal si lo vota el 30% de los presentes.', 'Utilizar exclusivamente pintura sintética aprobada por la policía de la Ciudad.'], 1, 'El programa de conservación edilicia delega sobre la administración y la persona jurídica del consorcio la obligación absoluta de velar por la estabilidad estructural de frentes, molduras y balcones para evitar caídas a la calle.'),
(3, '¿Qué consecuencia legal o administrativa afronta un consorcio o administrador ante el incumplimiento grave de las normas de conservación de ascensores o matafuegos ante una inspección de la AGC?', ['Multas severas y posible clausura preventiva de las instalaciones o equipos riesgosos.', 'Una simple amonestación verbal sin registración en las bases informáticas de la Ciudad.', 'Exención impositiva por un año fiscal en las tasas generales de alumbrado, barrido y limpieza.', 'La transferencia automática de la propiedad del edificio al dominio privado del Gobierno de la Ciudad.'], 0, 'La falta de cumplimiento preventivo en elementos de seguridad de alta criticidad (ascensores/matafuegos) faculta a los inspectores de la AGC a dictar multas pecuniarias y la clausura inmediata preventiva de los equipos.'),
(3, 'En el marco del programa "Fachadas Seguras" de la AGC, ¿a partir de qué antigüedad del edificio se vuelve obligatorio presentar periódicamente el Certificado de Conservación de Fachadas?', ['A partir de los 15 años de antigüedad del inmueble.', 'A partir de los 10 años de antigüedad del inmueble.', 'Únicamente cuando el edificio supera los 50 años de antigüedad en el catastro.', 'No depende de la antigüedad, sino de la cantidad de pisos que posea la estructura edilicia.'], 0, 'La Ley 257 (modificada por la Ley 6.116) fue abrogada por la Ley 6.438 (art. 119), que sustituyó el Título 5 del Código de Edificación (art. 111): hoy la obligación está en el art. 5.1.2, "Conservación de Fachadas". El Certificado de Conservación se exige desde los 15 años de antigüedad. La periodicidad es escalonada según la antigüedad: de 15 a 25 años, cada 15 años; más de 25 a 35, cada 12; más de 35 a 45, cada 10; más de 45 a 55, cada 9; más de 55 a 70, cada 5; y más de 70 años, cada 4 años.'),
(3, 'El sistema informatizado implementado por la AGC que sustituyó el histórico soporte físico en papel para registrar las firmas de inspecciones de mantenimiento se denomina:', ['Sistema de Gestión de Expedientes Electrónicos Nacionales.', 'Libro Digital de Conservación (Elevadores / Fachadas / IFCI).', 'Registro Único de Contratos Inmobiliarios de la CABA.', 'Aplicación Móvil miBA de Alerta Temprana de Siniestros.'], 1, 'El Libro Digital de Conservación de la AGC digitalizó e informatizó el asentamiento técnico directo de reparaciones por parte de los proveedores autorizados, eliminando las firmas en soporte de papel físico. No debe confundirse con el Libro de Inspecciones Digital para consorcios (Disposición 751/DGFYCO/26), que registra las inspecciones que realiza la AGC.'),
(3, '¿Quién es el profesional idóneo legalmente facultado para confeccionar el Informe Técnico de Fachadas Seguras a presentar ante la AGC a nombre del consorcio?', ['El encargado del edificio que cuente con más de 10 años de antigüedad en sus funciones de maestranza.', 'Un profesional con título habilitante y matrícula activa de Arquitecto o Ingeniero Civil.', 'El presidente del Consejo de Propietarios electo en la última asamblea extraordinaria.', 'Cualquier idóneo que realice tareas de pintura y albañilería en la zona de la Comuna correspondiente.'], 1, 'La presentación del Informe Técnico de Fachadas Seguras ante el Gobierno de la Ciudad exige la firma e incumbencia profesional de un Arquitecto o Ingeniero Civil matriculado en sus respectivos consejos de ley.'),
# ------------------------------------------------------------------ PREGUNTAS NUEVAS (1 a 9)
(4, "Si el consorcio decide dejar de ofrecer un servicio (por ejemplo, se anula la pileta o el gimnasio), ¿corresponde bajar de categoría al encargado y reducirle su sueldo?", [
    "Sí, porque su categoría está atada a los servicios que efectivamente presta el edificio.",
    "No, por el principio de intangibilidad del salario y derechos adquiridos (LCT y CCT SUTERH); no se le puede recortar el sueldo ni bajar la categoría alcanzada.",
    "Sí, pero se debe compensar con un bono anual.",
    "No, salvo que la asamblea lo apruebe por unanimidad."], 1,
    "El Art. 6 del CCT 589/10 dice expresamente que la supresión de algún servicio central no implica bajar de categoría al trabajador, y el Art. 15 (inc. 4) impide disminuir sueldos ya vigentes. Rige además el principio de intangibilidad del salario: quitar un servicio no permite al consorcio rebajar la remuneración ni la categoría adquirida."),
(1, "Según el Código Civil y Comercial (Art. 2067 inc. i), si un interesado solicita el certificado de deudas y créditos del consorcio, ¿en qué plazo debe expedirlo el administrador?", [
    "24 horas hábiles.",
    "5 días hábiles.",
    "3 días hábiles.",
    "10 días corridos."], 2,
    "El Código Civil y Comercial establece expresamente un plazo de 3 días hábiles para expedir este certificado, que debe incluir reclamos judiciales y seguros vigentes."),
(1, "En una asamblea se vota una propuesta con los propietarios presentes, pero no se alcanza la mayoría de la totalidad de los propietarios. ¿Cómo debe proceder el administrador?", [
    "Convocar de inmediato a una nueva asamblea para repetir la votación.",
    "Comunicar de forma fehaciente lo decidido a los propietarios ausentes y esperar 15 días: si no hay oposición de la mayoría, la decisión queda firme.",
    "Tomar la votación del momento como decisión definitiva y ejecutarla.",
    "Pedir al Registro Público de Administradores que valide la decisión."], 1,
    "Según el Art. 2060 del CCyC, la decisión adoptada por los presentes se notifica de forma fehaciente a los ausentes, quienes tienen 15 días corridos para oponerse. Si no se reúne la oposición de la mayoría de la totalidad de los propietarios, la decisión se considera aprobada. No se repite la asamblea ni se ejecuta antes de que venza ese plazo."),
(2, "El proveedor del servicio de ascensores del consorcio incumple gravemente sus obligaciones. ¿Qué debe hacer el administrador?", [
    "Denunciar al proveedor ante el Registro Público de Administradores (RPA).",
    "Analizar lo ocurrido, las cláusulas del contrato y el perjuicio al consorcio, y de corresponder intimar y prescindir del contrato.",
    "Prescindir del contrato de inmediato, sin analizar qué pasó ni las cláusulas de rescisión.",
    "Retenerle los pagos de otros consorcios que el proveedor atiende."], 1,
    "El RPA (Registro Público de Administradores) regula y sanciona exclusivamente a los administradores de consorcios en CABA, no a los proveedores (como plomeros o empresas de limpieza). La acción correcta es rescindir el contrato."),
(2, "Según la Disposición 3644/DGDYPC/26 (BOCBA 10/09/2026), ¿qué carácter tiene el código QR o hipervínculo en las liquidaciones de expensas de CABA?", [
    "Es obligatorio: su omisión constituye infracción a la Ley 941 y puede ser sancionada.",
    "Es facultativo, informativo y voluntario: permite acceder al Reglamento de Propiedad Horizontal del consorcio, y su omisión no constituye incumplimiento ni genera sanción.",
    "Es obligatorio solo en consorcios de más de 20 unidades funcionales y sirve como medio de pago.",
    "Es obligatorio y sirve exclusivamente para acceder al recibo de sueldo del encargado."], 1,
    "La Disposición 3644/DGDYPC/26 dejó sin efecto el Manual de Buenas Prácticas Consorciales y estableció que incorporar a la liquidación un QR, hipervínculo o enlace de acceso al Reglamento de Propiedad Horizontal es facultativo, informativo y voluntario. Su omisión no es incumplimiento de la Ley 941 ni da lugar por sí sola a sanción. Atención: material de estudio anterior a septiembre de 2026 lo presenta como obligatorio."),
(2, "De acuerdo con la Ley 941 de CABA, si un propietario solicita ver la documentación del consorcio, ¿cuál es el plazo máximo que tiene el administrador para ponerla a disposición?", [
    "48 horas hábiles.",
    "72 horas hábiles.",
    "5 días hábiles.",
    "15 días corridos."], 2,
    "Según el Art. 9 inc. f) de la Ley 941, el administrador debe poner a disposición de los consorcistas la documentación del consorcio en un plazo no mayor a cinco (5) días hábiles."),
(1, "Si el administrador omite convocar a una asamblea, ¿qué alternativas legales y válidas prevé el Código Civil y Comercial para los consorcistas?", [
    "Solo pueden solicitar una asamblea judicial si logran reunir la firma del 5% de los propietarios.",
    "Únicamente el Registro Público de Administradores (RPA) puede intimar al administrador a realizarla.",
    "Puede convocarla el Consejo de Propietarios; también pueden autoconvocarse (con 2/3) o tomar decisiones por unanimidad (100%) de todos los propietarios sin necesidad de asamblea.",
    "Cualquier propietario individual puede convocarla enviando cartas documento al resto de los vecinos."], 2,
    "Según los Arts. 2058 y 2059 del CCyC, si el administrador omite el llamado, el Consejo de Propietarios asume la facultad de convocarla. Además, es válido autoconvocarse (aprobando temario con 2/3) o decidir por unanimidad (100%) sin asamblea. IMPORTANTE: Para solicitar la asamblea judicial (Art. 2063), la ley exige el 10% de los propietarios, no el 5%, por lo que esa opción suele ser una trampa de examen."),
(1, "En la práctica habitual, si una asamblea toma una decisión válida (cumpliendo con la convocatoria y mayorías de ley) para agregar nuevos servicios comunes o 'amenities' al edificio, ¿cuál es la responsabilidad del administrador frente a esto?", [
    "Puede negarse a acatarla si considera que encarece las expensas, ya que él es el representante legal y responde con su patrimonio personal.",
    "Debe ejecutar la decisión obligatoriamente, ya que la asamblea es el órgano soberano. Además, deberá ajustar la categoría del edificio y del encargado según los nuevos servicios.",
    "Solo debe ejecutar la decisión si la asamblea fue convocada por vía judicial, de lo contrario carece de validez legal para sumar servicios.",
    "Debe renunciar a su cargo si no está de acuerdo, porque las decisiones sobre amenities son facultad exclusiva del Consejo de Propietarios."], 1,
    "Basado en el Art. 2067 del CCyC (Derechos y obligaciones del administrador): el administrador tiene la obligación de ejecutar las decisiones válidas de la asamblea. Además, en la práctica habitual, al sumar amenities, el administrador es responsable de actualizar la categoría del edificio según el CCT de SUTERH, lo que impacta en el sueldo del encargado."),
(4, "Según el Convenio Colectivo de Trabajo (CCT 589/10 - SUTERH) aplicable a la administración de consorcios, ¿cómo impacta la cantidad de servicios centrales o 'amenities' (agua caliente, calefacción, natatorio, gimnasio, salón de usos múltiples, etc.) en la categorización del edificio?", [
    "La categoría se define únicamente por la cantidad de unidades funcionales (departamentos) y metros cuadrados, sin importar los amenities.",
    "Edificio de 1ra categoría: 3 o más servicios; 2da categoría: 2 servicios; 3ra categoría: 1 servicio; 4ta categoría: sin servicios centrales.",
    "Todos los edificios que posean al menos un amenity (ejemplo: pileta) son considerados automáticamente de 1ra categoría.",
    "Lo define la asamblea anualmente por mayoría simple, pudiendo bajar la categoría si deciden no utilizar la pileta en invierno."], 1,
    "El Art. 6 del CCT 589/10 enumera los servicios centrales: agua caliente, calefacción, compactador o incinerador de residuos, gas envasado central, desagote de cámara séptica, ablandador de agua, natatorio, gimnasio, saunas, cancha de paddle, tenis o squash, salón de usos múltiples, solarium y lavandería. Según cuántos existan: 1ra categoría, tres o más; 2da, dos; 3ra, uno; 4ta, ninguno. Ni la vigilancia ni el jardín figuran en esa lista (el jardín da lugar a un plus, Art. 15 inc. 5). Y la supresión de un servicio central no baja la categoría del trabajador."),
]

S = st.session_state

# ---------------------------------------------------------------- historial
@st.cache_resource
def _memoria():
    return {"lock": threading.Lock(), "items": []}

def leer_historial():
    try:
        return json.loads(HIST.read_text(encoding="utf-8"))
    except Exception:
        return list(_memoria()["items"])

def _guardar(rec):
    """Guarda en memoria y en archivo. Llamar siempre con el lock tomado."""
    m = _memoria()
    m["items"].append(rec)
    try:
        datos = json.loads(HIST.read_text(encoding="utf-8")) if HIST.exists() else []
        datos.append(rec)
        HIST.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

def registrar(rec):
    with _memoria()["lock"]:
        _guardar(rec)

def normalizar(nombre):
    return " ".join(nombre.split())

def reservar(nombre):
    """Registra el inicio de un intento. Devuelve False si el nombre ya lo usa otra persona."""
    clave = nombre.casefold()
    with _memoria()["lock"]:
        if clave not in S.propios:
            usados = {r["nombre"].strip().casefold() for r in leer_historial()}
            if clave in usados:
                return False
        _guardar(dict(nombre=nombre, fecha=datetime.now().strftime("%Y-%m-%d %H:%M"), inicio=True))
    S.propios.add(clave)
    return True

# ---------------------------------------------------------------- estado
def orden_nuevo():
    """Orden aleatorio de las preguntas (como en un examen real, las áreas van mezcladas)."""
    o = list(range(len(Q)))
    random.shuffle(o)
    return o

def minimo_aprobacion(total):
    return math.ceil(total * APROBAR / 100)

def nuevo(order, conservar_usuario=True):
    usuario = S.get("usuario", "") if conservar_usuario else ""
    S.order, S.pos, S.ans, S.stage, S.confirm = order, 0, {}, "inicio", False
    S.deadline, S.used, S.fx, S.saved = None, 0, False, False
    S.run = S.get("run", 0) + 1
    S.usuario = usuario
    S.perm = {n: random.sample(range(4), 4) for n in range(len(Q))}
    S.setdefault("mis", [])
    S.setdefault("propios", set())

def comenzar(nombre):
    nombre = normalizar(nombre)
    if not reservar(nombre):
        return False
    S.usuario = nombre
    S.deadline = time.time() + DURACION
    S.stage = "examen"
    return True

def resumen():
    total = len(S.order)
    ok = [n for n in S.order if S.ans.get(n) == Q[n][3]]
    return total, ok

def terminar():
    S.used = min(DURACION, DURACION - (S.deadline - time.time()))
    S.stage, S.confirm, S.fx = "fin", False, True
    if not S.saved:
        total, ok = resumen()
        pct = len(ok) / total * 100
        areas = {}
        for n in S.order:
            a = areas.setdefault(str(Q[n][0]), [0, 0]); a[1] += 1; a[0] += n in ok
        rec = dict(nombre=S.usuario, fecha=datetime.now().strftime("%Y-%m-%d %H:%M"), correctas=len(ok), total=total,
                   nota=max(1.0, round(pct / 10, 1)), aprobado=len(ok) >= minimo_aprobacion(total),
                   segundos=int(S.used), areas=areas)
        registrar(rec)
        S.mis.append(rec)
        S.saved = True

if "stage" not in S:
    nuevo(orden_nuevo())

# ---------------------------------------------------------------- pantallas
@st.fragment(run_every=1)
def reloj():
    resto = int(S.deadline - time.time())
    if resto <= 0:
        terminar()
        st.rerun()
    m, s = divmod(resto, 60)
    st.metric("⏱️ Tiempo restante", f"{m:02d}:{s:02d}")

def inicio():
    total = len(S.order)
    minimo = minimo_aprobacion(total)
    st.write(f"""**Formato:** opción múltiple, una sola respuesta correcta · **{total} preguntas** · **{DURACION // 60} minutos**  
**Aprobación:** nota mínima 6 (al menos {minimo} de {total} correctas). Las incorrectas o en blanco no restan.  
**Feedback:** después de cada respuesta ves si acertaste y cuál era la correcta.  
Las preguntas aparecen mezcladas y las opciones cambian de orden en cada intento.  
Podés repetir el simulacro todas las veces que quieras.""")
    nombre = st.text_input("Tu nombre o apodo (para registrar tu intento)", value=S.usuario, max_chars=30)
    if st.button("Comenzar examen", type="primary", disabled=len(normalizar(nombre)) < 2):
        if comenzar(nombre):
            st.rerun()
        else:
            st.error("Ese nombre o apodo ya lo usó otra persona. Elegí uno distinto (por ejemplo, agregá una inicial o un número).")

def examen():
    if time.time() >= S.deadline:
        terminar(); st.rerun()
    reloj()
    total = len(S.order)
    n = S.order[S.pos]
    area, q, opts, a, expl = Q[n]
    perm = S.perm[n]
    st.progress(S.pos / total)
    st.caption(f"{S.usuario} · Pregunta {S.pos + 1} de {total} · {AREAS[area]}")
    st.subheader(q)
    if n not in S.ans:
        sel = st.radio("Opciones", range(4), index=None, key=f"q{S.run}_{n}",
                       format_func=lambda i: f"{'ABCD'[i]}) {opts[perm[i]]}", label_visibility="collapsed")
        c1, c2 = st.columns(2)
        if c1.button("Responder", type="primary", disabled=sel is None):
            S.ans[n] = perm[sel]; st.rerun()
        if c2.button("Omitir (queda en blanco)"):
            S.ans[n] = None; st.rerun()
        return
    elegida = S.ans[n]
    for i, oi in enumerate(perm):
        txt = f"{'ABCD'[i]}) {opts[oi]}"
        if oi == a:
            st.markdown(f"✅ **{txt}**")
        elif oi == elegida:
            st.markdown(f"❌ ~~{txt}~~")
        else:
            st.markdown(f"◻️ {txt}")
    letra = "ABCD"[perm.index(a)]
    if elegida == a:
        st.success(f"¡Correcto! La respuesta correcta es la {letra}.")
    elif elegida is None:
        st.warning(f"Pregunta en blanco. La respuesta correcta era la {letra}.")
    else:
        st.error(f"Incorrecta. La respuesta correcta es la {letra}) {opts[a]}")
    st.info(expl)
    ultima = S.pos + 1 >= total
    if st.button("Ver resultados" if ultima else "Siguiente", type="primary"):
        if ultima:
            terminar()
        else:
            S.pos += 1
        st.rerun()

def resultados():
    total, ok = resumen()
    en_blanco = [n for n in S.order if S.ans.get(n, None) is None]
    mal = [n for n in S.order if n not in ok]
    pct = len(ok) / total * 100
    nota = max(1.0, round(pct / 10, 1))
    minimo = minimo_aprobacion(total)
    aprobado = len(ok) >= minimo

    # Aviso emergente (una sola vez por intento)
    if aprobado and not S.get(f"toast_{S.run}"):
        S[f"toast_{S.run}"] = True
        st.toast("🥂 ¡Brindemos por ese resultado!", icon="🎉")

    st.title(f"Resultado de {S.usuario}")
    m, s = divmod(int(S.used), 60)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nota (1 a 10)", f"{nota:.1f}")
    c2.metric("Porcentaje", f"{pct:.0f}%")
    c3.metric("Correctas", f"{len(ok)} / {total}")
    c4.metric("Tiempo", f"{m:02d}:{s:02d}")
    st.progress(pct / 100, text=f"{pct:.1f}% de aciertos · mínimo para aprobar: {APROBAR}%")

    if aprobado:
        st.success("🥂 ¡APROBADO! Alcanzaste el mínimo de 6 puntos. ¡Brindemos!")
    else:
        st.error(f"NO APROBADO. Necesitabas {minimo} correctas y lograste {len(ok)}. Te faltaron {minimo - len(ok)}. ¡A repetir!")

    if en_blanco:
        st.caption(f"Preguntas en blanco: {len(en_blanco)} (no restan puntos).")

    filas = []
    for k, nombre in AREAS.items():
        idx = [n for n in S.order if Q[n][0] == k]
        if idx:
            b = sum(S.ans.get(n) == Q[n][3] for n in idx)
            filas.append({"Área": nombre, "Correctas": b, "Total": len(idx), "Dominio": b / len(idx) * 100})
    df = pd.DataFrame(filas).sort_values("Dominio")
    st.subheader("Rendimiento por área")
    st.dataframe(df, hide_index=True, column_config={
        "Dominio": st.column_config.ProgressColumn("Dominio", min_value=0, max_value=100, format="%d%%")})
    peor = df.iloc[0]
    if peor["Dominio"] < 100:
        st.warning(f"Donde más te costó: **{peor['Área']}** ({peor['Dominio']:.0f}%). Es lo que más te conviene practicar.")
    else:
        st.success("Dominio del 100% en todas las áreas.")

    if mal:
        st.subheader("Para repasar")
        for n in mal:
            area, q, opts, a, expl = Q[n]
            with st.expander(f"[{AREAS[area]}] {q}"):
                el = S.ans.get(n)
                st.write("❌ Tu respuesta: " + (opts[el] if el is not None else "en blanco"))
                st.write(f"✅ Correcta: {opts[a]}")
                st.caption(expl)

    if len(S.mis) > 1:
        st.subheader("Tus intentos de esta sesión")
        st.dataframe(pd.DataFrame([{"Intento": i + 1, "Fecha": r["fecha"], "Correctas": f"{r['correctas']}/{r['total']}",
                                    "Nota": r["nota"], "Resultado": "Aprobado" if r["aprobado"] else "Desaprobado"}
                                   for i, r in enumerate(S.mis)]), hide_index=True)
    b1, b2 = st.columns(2)
    if b1.button("🔁 Repetir el examen", type="primary"):
        nuevo(orden_nuevo()); st.rerun()
    if b2.button("Cambiar de nombre"):
        nuevo(orden_nuevo(), conservar_usuario=False); st.rerun()
    st.divider()
    st.markdown(f"## Nota final: {nota:.1f} / 10 — {'APROBADO 🥂' if aprobado else 'NO APROBADO'}")

    # FESTEJO: globos 30 s + fuegos 10 s + cartel. Va al final de la página y
    # se mantiene montado mientras estés en los resultados (así no se corta).
    if aprobado and S.fx:
        festejo_aprobado(token=f"{S.run}-{len(S.mis)}")

def personas_que_intentaron():
    return len({r["nombre"].strip().lower() for r in leer_historial()})

st.title("🏢 Simulacro RPA · Administrador de Consorcios (CABA)")
contador = st.empty()
{"inicio": inicio, "examen": examen, "fin": resultados}[S.stage]()
contador.metric("👥 Personas que intentaron el examen", personas_que_intentaron())
