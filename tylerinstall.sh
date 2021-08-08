cd /opt && git clone https://github.com/m-schuetz/LAStools.git && cd LAStools/LASzip && mkdir build && cd build && \
cmake -DCMAKE_BUILD_TYPE=Release .. && make && make install && ldconfig

cd /opt && git clone -b using_laszip https://github.com/potree/PotreeConverter.git && cd PotreeConverter && \
sed -i -e 's/#include <filesystem>/#include <experimental\/filesystem>/g' PotreeConverter/src/main.cpp && \
sed -i -e 's/namespace fs = std::filesystem;/namespace fs = std::experimental::filesystem;/g' PotreeConverter/src/main.cpp && \
sed -i -e 's/#include <filesystem>/#include <experimental\/filesystem>/g' PotreeConverter/src/BINPointReader.cpp && \
sed -i -e 's/namespace fs = std::filesystem;/namespace fs = std::experimental::filesystem;/g' PotreeConverter/src/BINPointReader.cpp && \
sed -i -e 's/#include <filesystem>/#include <experimental\/filesystem>/g' PotreeConverter/include/PointReader.h && \
sed -i -e 's/namespace fs = std::filesystem;/namespace fs = std::experimental::filesystem;/g' PotreeConverter/include/PointReader.h && \
sed -i -e 's/#include <filesystem>/#include <experimental\/filesystem>/g' PotreeConverter/include/stuff.h && \
sed -i -e 's/namespace fs = std::filesystem;/namespace fs = std::experimental::filesystem;/g' PotreeConverter/include/stuff.h && \
sed -i -e 's/#include <filesystem>/#include <experimental\/filesystem>/g' PotreeConverter/src/LASPointReader.cpp && \
sed -i -e 's/#include "laszip_dll.h"/#include "laszip_api.h"/g' PotreeConverter/src/* && \
sed -i -e 's/#include "laszip_dll.h"/#include "laszip_api.h"/g' PotreeConverter/include/* && \
sed -i -e 's/namespace fs = std::filesystem;/namespace fs = std::experimental::filesystem;/g' PotreeConverter/src/LASPointReader.cpp && \
sed -i -e 's/#include <filesystem>/#include <experimental\/filesystem>/g' PotreeConverter/src/PotreeConverter.cpp && \
sed -i -e 's/namespace fs = std::filesystem;/namespace fs = std::experimental::filesystem;/g' PotreeConverter/src/PotreeConverter.cpp && \
sed -i -e 's/#include <filesystem>/#include <experimental\/filesystem>/g' PotreeConverter/src/PotreeWriter.cpp && \
sed -i -e 's/namespace fs = std::filesystem;/namespace fs = std::experimental::filesystem;/g' PotreeConverter/src/PotreeWriter.cpp && \
sed -i -e 's/writer->write(reader->getPoint());/Potree::Point point = reader->getPoint();\nwriter->write(point);/g' PotreeConverter/src/PotreeWriter.cpp && \
sed -i '1 a #include <cstring>' PotreeConverter/src/BINPointReader.cpp && \
mkdir build && cd build && \
cmake -DCMAKE_BUILD_TYPE=Release -DLASZIP_INCLUDE_DIRS=/opt/LAStools/LASzip/dll -DLASZIP_LIBRARY=/usr/local/lib/liblaszip.so .. && \
make && make install && cp -r /opt/PotreeConverter/PotreeConverter/resources /opt/PotreeConverter/build/resources

cd /opt && git clone https://github.com/potree/potree.git && \
cd potree && \
npm install && \
sed -i -e "s/https: false,/https: false,\n                host: '0.0.0.0',/g" gulpfile.js && \
touch examples/potcon.html && \
rm -rf pointclouds/*
