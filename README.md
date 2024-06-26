# ChooseChef
# API para contratación de chefs a domicilio y catering

**Descripción general:** 
Chef a la carta es una plataforma que conecta a usuarios que buscan servicios culinarios con chefs profesionales que ofrecen sus habilidades en la comodidad del hogar o para eventos especiales. La API del servidor es la piedra angular de esta plataforma, proporcionando la infraestructura digital para gestionar usuarios, chefs, pedidos, pagos y comunicación entre las partes involucradas.

**Motivación:** 
El proyecto surge de la necesidad de brindar una solución innovadora y conveniente para acceder a servicios culinarios de alta calidad. La plataforma busca eliminar las barreras de la cocina tradicional, ofreciendo a los usuarios una experiencia gastronómica personalizada y a los chefs la oportunidad de ampliar su alcance y clientela.

**Público objetivo:** 
La API está dirigida a dos grupos principales:
    + Clientes: Personas que buscan contratar chefs a domicilio para cenas privadas, eventos especiales o catering para fiestas.
    + Chefs: Profesionales de la cocina que desean ofrecer sus servicios a través de la plataforma y ampliar su base de clientes.

**Funcionalidades:**
    + Gestión de usuarios: Registro, autenticación, actualización de perfiles y preferencias de usuarios tanto para clientes como para chefs.
    + Administración de chefs: Registro, autenticación, gestión de perfiles, disponibilidad, especialidades culinarias y zonas de servicio de los chefs.
    + Solicitud de eventos: Creación, gestión y seguimiento de los eventos por parte de los usuarios, incluyendo selección de chefs, menús, fechas y ubicaciones.
    + Evaluaciones y reseñas: Permitir a usuarios y chefs dejar comentarios y valoraciones sobre sus experiencias para fomentar la confianza y la transparencia

**Tecnologías:**
Lenguaje de programación: FastApi con Python 
Base de datos: MySQL
Alojamiento: AWS
Herramientas de desarrollo: Git, Vercel

**Beneficios:**
Para usuarios:
    + Acceso a una amplia red de chefs profesionales con diferentes estilos y especialidades.
    + Comodidad de disfrutar de una experiencia gastronómica personalizada en la comodidad del hogar o en eventos especiales.
    + Posibilidad de evaluar y calificar a los chefs para tomar decisiones informadas.
Para chefs:
    + Oportunidad de ampliar su base de clientes y llegar a nuevos comensales.
    + Plataforma flexible para gestionar su disponibilidad, menús y precios.
    + Posibilidad de recibir comentarios y valoraciones para mejorar su oferta culinaria.

**Conclusión:**
La API de Chef a la carta se presenta como una solución innovadora y tecnológica para el sector culinario, conectando a usuarios que buscan experiencias gastronómicas únicas con chefs profesionales que desean compartir su talento. Con un enfoque en la facilidad de uso, la seguridad y la transparencia, la plataforma tiene el potencial de transformar la forma en que las personas disfrutan de la comida y apoyan a los chefs locales.

**Iniciar el servidor**
    uvicorn main:app --reload 
    
**Iniciar batería de test**
    pytest