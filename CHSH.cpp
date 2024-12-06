#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <omp.h>

#include <random>
#include <sstream>

#include "State.h"

struct Game {
	bool x; // send to Alice
	bool y; // send to Bob
	bool a; // Alice return
	bool b; // Bob return
};

std::vector<Game> PlayRandom(int n) {
	std::vector<Game> games(n);

#pragma omp parallel
	{
		std::random_device rd;
		std::mt19937 gen(rd() + omp_get_thread_num());
		std::bernoulli_distribution referee(0.5);

#pragma omp for
		for (int i = 0; i < n; i++) {
			bool x = referee(gen);
			bool y = referee(gen);
			bool a = referee(gen);
			bool b = referee(gen);
			games[i] = { x, y, a, b };
		}
	}

	return games;
}

std::vector<Game> PlayClassical(int n, bool Strategy = false) {
	std::vector<Game> games(n);

#pragma omp parallel
	{
		std::random_device rd;
		std::mt19937 gen(rd() + omp_get_thread_num());
		std::bernoulli_distribution referee(0.5);

#pragma omp for
		for (int i = 0; i < n; i++) {
			bool x = referee(gen);
			bool y = referee(gen);
			bool a = Strategy;
			bool b = Strategy;
			games[i] = { x, y, a, b };
		}
	}

	return games;
}

std::vector<Game> PlayQuantum(int n, double err, double diff_a, double diff_0, double diff_b, bool Alice_first = true) {
	std::vector<Game> games(n);

#pragma omp parallel
	{
		std::random_device rd;
		std::mt19937 gen(rd() + omp_get_thread_num());
		std::uniform_real_distribution<> uniform(0, 1);
		std::bernoulli_distribution referee(0.5);

#pragma omp for
		for (int i = 0; i < n; i++) {
			State state(err);
			bool x = referee(gen);
			bool y = referee(gen);
			double theta_a = x ? diff_a : 0.0; // Alice's measurement
			double theta_b = diff_0 + (y ? diff_b : 0.0); // Bob's measurement
			if (Alice_first) {
				bool a = state.Measure(theta_a, uniform(gen));
				bool b = state.Measure(theta_b, uniform(gen));
				games[i] = { x, y, a, b };
			}
			else {
				bool b = state.Measure(theta_b, uniform(gen));
				bool a = state.Measure(theta_a, uniform(gen));
				games[i] = { x, y, a, b };
			}
		}
	}
	return games;
}

struct GameResult {
	int n00, n01, n10, n11; // number of games x, y values
	int w00, w01, w10, w11; // number of wins with x, y values
	double WinRate00; // win rate with x = 0 and y = 0
	double WinRate01; // win rate with x = 0 and y = 1
	double WinRate10; // win rate with x = 1 and y = 0
	double WinRate11; // win rate with x = 1 and y = 1
	int n, w; // total number of games and wins
	double WinRate; // overall win rate

	std::string to_string() const {
		std::ostringstream oss;
		oss << "Winning rate with x = 0 and y = 0: " << WinRate00 << "( " << w00 << " / " << n00 << " )" << std::endl
			<< "Winning rate with x = 0 and y = 1: " << WinRate01 << "( " << w01 << " / " << n01 << " )" << std::endl
			<< "Winning rate with x = 1 and y = 0: " << WinRate10 << "( " << w10 << " / " << n10 << " )" << std::endl
			<< "Winning rate with x = 1 and y = 1: " << WinRate11 << "( " << w11 << " / " << n11 << " )" << std::endl
			<< "Overall winning rate: " << WinRate << "( " << w << " / " << n << " )";
		return oss.str();
	}
};

GameResult Analyze(const std::vector<Game>& games) {

	int n = games.size();
	int n00 = 0, n01 = 0, n10 = 0, n11 = 0;
	int w00 = 0, w01 = 0, w10 = 0, w11 = 0;

	for (const Game& game : games) {

		if (!game.x && !game.y) { // x = 0, y = 0
			n00++;
			if (!(game.a ^ game.b)) { // a ^ b = 0
				w00++;
			}
		}

		else if (!game.x && game.y) { // x = 0, y = 1
			n01++;
			if (!(game.a ^ game.b)) { // a ^ b = 0
				w01++;
			}
		}

		else if (game.x && !game.y) { // x = 1, y = 0
			n10++;
			if (!(game.a ^ game.b)) { // a ^ b = 0
				w10++;
			}
		}

		else { // x = 1, y = 1
			n11++;
			if (game.a ^ game.b) { // a ^ b = 1
				w11++;
			}
		}
	}

	int w = w00 + w01 + w10 + w11;
	double WinRate00 = (double)w00 / n00;
	double WinRate01 = (double)w01 / n01;
	double WinRate10 = (double)w10 / n10;
	double WinRate11 = (double)w11 / n11;
	double WinRate = (double)w / n;
	return { n00, n01, n10, n11, w00, w01, w10, w11, WinRate00, WinRate01, WinRate10, WinRate11, n, w, WinRate };
}

namespace py = pybind11;

PYBIND11_MODULE(CHSH, m) {
	m.doc() = "CHSH simulation module";

	py::class_<Game>(m, "Game")
		.def_readwrite("x", &Game::x)
		.def_readwrite("y", &Game::y)
		.def_readwrite("a", &Game::a)
		.def_readwrite("b", &Game::b);

	m.def("PlayRandom", &PlayRandom,
		py::arg("n"),
		"Simulate games and return a list of results.");

	m.def("PlayClassical", &PlayClassical,
		py::arg("n"),
		py::arg("Strategy") = false,
		"Simulate games and return a list of results.");

	m.def("PlayQuantum", &PlayQuantum,
		py::arg("n"),
		py::arg("err"),
		py::arg("diff_a"),
		py::arg("diff_0"),
		py::arg("diff_b"),
		py::arg("Alice_first") = true,
		"Simulate games and return a list of results.");

	py::class_<GameResult>(m, "GameResult")
		.def_readwrite("n00", &GameResult::n00)
		.def_readwrite("n01", &GameResult::n01)
		.def_readwrite("n10", &GameResult::n10)
		.def_readwrite("n11", &GameResult::n11)
		.def_readwrite("w00", &GameResult::w00)
		.def_readwrite("w01", &GameResult::w01)
		.def_readwrite("w10", &GameResult::w10)
		.def_readwrite("w11", &GameResult::w11)
		.def_readwrite("WinRate00", &GameResult::WinRate00)
		.def_readwrite("WinRate01", &GameResult::WinRate01)
		.def_readwrite("WinRate10", &GameResult::WinRate10)
		.def_readwrite("WinRate11", &GameResult::WinRate11)
		.def_readwrite("n", &GameResult::n)
		.def_readwrite("w", &GameResult::w)
		.def_readwrite("WinRate", &GameResult::WinRate)
		.def("__repr__", [](const GameResult& r) { return r.to_string(); });

	m.def("Analyze", &Analyze,
		py::arg("games"),
		"Analyze a list of games and return a summary.");
}
