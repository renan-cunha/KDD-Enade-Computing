# enade data
mkdir -p enade


curl http://download.inep.gov.br/microdados/Enade_Microdados/microdados_enade_2005.zip --output microdados_enade_2005.zip
unzip -d enade/enade2005 microdados_enade_2005.zip

curl http://download.inep.gov.br/microdados/Enade_Microdados/microdados_Enade_2017_portal_2018.10.09.zip --output microdados_enade_2017.zip 
unzip -d enade/enade2017 microdados_enade_2017.zip

curl http://download.inep.gov.br/microdados/Enade_Microdados/microdados_enade_2014.zip --output microdados_enade_2014.zip 
unzip -d enade/enade2014 microdados_enade_2014.zip

curl http://download.inep.gov.br/microdados/Enade_Microdados/microdados_enade_2011.zip --output microdados_enade_2011.zip
unzip -d enade/enade2011 microdados_enade_2011.zip

curl http://download.inep.gov.br/microdados/Enade_Microdados/microdados_enade_2008.zip --output microdados_enade_2008.zip
unzip -d enade/enade2008 microdados_enade_2008.zip

