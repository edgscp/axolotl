docker login
git clone https://github.com/edgscp/axolotl.git
git checkout -b classilex-3 origin/classilex-3
docker build -t david1155/axolotl-base:main-base -f Dockerfile-base .
docker push david1155/axolotl-base:main-base

docker build -t david1155/axolotl:classilex-3 -f Dockerfile .
docker push david1155/axolotl:classilex-3

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
