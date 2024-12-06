#pragma once

#include <vector>
#include <cmath>

class State {

public:

	State(double err) {
		data = std::vector<double>(16);
		// diagonal elements
		data[0] = 0.5 - 0.25 * err;
		data[5] = 0.25 * err;
		data[10] = 0.25 * err;
		data[15] = 0.5 - 0.25 * err;
		// off-diagonal elements
		data[3] = 0.5 * (1.0 - err);
		data[12] = 0.5 * (1.0 - err);
	}

	bool Measure(double theta, double uniform) {

		const double s = std::sin(theta), c = std::cos(theta);

		if (bit) { // both bits exist
			bit = false; // distructive measurement
			std::vector<double> newData(4); // new state
			// probability of measuring 0
			double p = c * c * (data[0] + data[5]) + c * s * (data[2] + data[7] + data[8] + data[13]) + s * s * (data[10] + data[15]);
			bool result = uniform < p;
			if (result) { // measurement is 0
				newData[0] = (c * c * data[0] + c * s * (data[2] + data[8]) + s * s * data[10]) / p;
				newData[1] = (c * c * data[1] + c * s * (data[3] + data[9]) + s * s * data[11]) / p;
				newData[2] = (c * c * data[4] + c * s * (data[6] + data[12]) + s * s * data[14]) / p;
				newData[3] = (c * c * data[5] + c * s * (data[7] + data[13]) + s * s * data[15]) / p;
			}
			else { // measurement is 1
				newData[0] = (s * s * data[0] - c * s * (data[2] + data[8]) + c * c * data[10]) / (1.0 - p);
				newData[1] = (s * s * data[1] - c * s * (data[3] + data[9]) + c * c * data[11]) / (1.0 - p);
				newData[2] = (s * s * data[4] - c * s * (data[6] + data[12]) + c * c * data[14]) / (1.0 - p);
				newData[3] = (s * s * data[5] - c * s * (data[7] + data[13]) + c * c * data[15]) / (1.0 - p);
			}
			data = newData;
			return result;
		}

		else { // only one qubit
			double p = c * c * data[0] + c * s * (data[1] + data[2]) + s * s * data[3];
			bool result = uniform < p;
			return result;
		}
	}

private:
	std::vector<double> data;
	bool bit = true;
};