#include "boost/python/numpy.hpp"
#include <iostream>
#include <stdexcept>
#include <algorithm>
#include <random>

namespace p = boost::python;
namespace np = boost::python::numpy;


double getData(np::ndarray array2d, int x, int y)
{
    auto strides = array2d.get_strides();
    return *reinterpret_cast<int *>(array2d.get_data() + y * strides[0] + x * strides[1]);
}

void setData(np::ndarray& array2d, int x, int y, double v)
{
    auto strides = array2d.get_strides();
    *reinterpret_cast<int *>(array2d.get_data() + y * strides[0] + x * strides[1]) = v;
}

int getAround(np::ndarray frame, int x, int y)
{
    int count = - int(getData(frame, x, y));
    for (int j = -1; j <= 1; j++)
        for (int i = -1; i <= 1; i++) 
            count += int(getData(frame, x + i, y + j));
    return count;
}


void lifegameUpdate(np::ndarray frame, np::ndarray nextFrame, float mutateRatio)
{
    if (frame.get_nd() != 2 || nextFrame.get_nd() != 2) {
        throw std::runtime_error("Error: array must be 2-demensional.");
    }
    size_t x = frame.shape(1);
    size_t y = frame.shape(0);
    if (x != nextFrame.shape(1) || y != nextFrame.shape(0)) {
        throw std::runtime_error("Error: frame and next frame must be same size.");
    }

    std::random_device rd;
    std::mt19937 mt(rd());
    std::uniform_real_distribution<double> score(0.0, 1.0);

    int count;
    int current;
    for (size_t j = 1; j < y - 1; j++) {
        for (size_t i = 1; i < x - 1; i++) {
            count = getAround(frame, i, j);
            current = getData(frame, i, j);
     
            if (current == 0 && count == 3) { 
                setData(nextFrame, i, j, 1);
            }
            else if (current == 1 && (count == 2 || count == 3)) {
                setData(nextFrame, i, j, 1);
            }
            else if (current == 1 && (count <= 1 || count >= 4)) {
                setData(nextFrame, i, j, 0);
            }
            else {
                setData(nextFrame, i, j, current);
            }

            // mutation
            if (score(mt) < mutateRatio) {
                setData(nextFrame, i, j, 1 - current);
            }
        }
    }
} 



/* BOOST_PYTHON_MODULE の引数は .so 名 */
BOOST_PYTHON_MODULE(liblifegame) {
  Py_Initialize();
  np::initialize();
  p::def("lifegame_update", lifegameUpdate);
}

