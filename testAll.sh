#!/bin/bash

cd testresult
rm *
cd ead
rm *
cd ../eac-cpf
rm *
cd ..

echo "************* EAD ************** "
echo "(01) /search/ead"
../searchEad.py

echo "(02) /search/ead (facets)"
../searchEadFacets.py

echo "(03) /search/ead (order)"
../searchEadOrder.py

echo "(04) /search/ead/docList"
../searchEadDoclist.py

echo "(05) /search/ead/docList (facets)"
../searchEadDoclistFacets.py

echo "(06) /search/ead/{id}/children"
../searchEadChildren.py

echo "(07) /search/ead/{id}/descendants"
../searchEadDescendants.py

echo "(08) /hierarchy/ead/{id}/ancestors"
../hierarchyEadAncestors.py

echo "(09) /hierarchy/ead/{id}/children"
../hierarchyEadChildren.py

echo "(10) /content/ead/archdesc"
../contentEadArchdesc.py

echo "(11) /content/ead/clevel"
../contentEadClevel.py

echo "(12) /download/ead"
cd ead
../../downloadEad.py
cd ..


echo "************* EAC-CPF ************** "
echo "(13) /search/eac-cpf"
../searchEac-cpf.py

echo "(14) /search/eac-cpf (facets)"
../searchEacFacets.py

echo "(15) /content/eac-cpf"
../contentEac-cpf.py

echo "(16) /download/eac-cpf"
cd eac-cpf
../../downloadEac-cpf.py
cd ..

echo "************** OVERVIEW ************** "
echo "(17) /institute/getInstitutes"
../instituteGetInstitutes.py

echo "(18) /institute/getDocs"
../instituteGetDocs.py

