import numpy as np

class AsianCallOption(object):
    def __init__(self, initial_price,
                 strike_price,
                 interest_rate,
                 volatility,
                 time_to_maturity: int,
                 time_partition_size: int,
                 spatial_partition_size: int):
        super(AsianCallOption, self).__init__()
        self.initial_price = initial_price
        self.strike_price = strike_price
        self.interest_rate = interest_rate
        self.volatility = volatility
        self.time_to_maturity = time_to_maturity
        self.time_partition_size = time_partition_size
        self.spatial_partition_size = spatial_partition_size

    def solve(self, spatial_size=3):
        self.spatial_size = spatial_size

        dt = self.time_to_maturity / self.time_partition_size
        dz = 2 * (self.spatial_size / self.spatial_partition_size)
        d = dt / dz ** 2

        u = np.zeros((self.time_partition_size+1, self.spatial_partition_size+1))
        #time = np.mslice[0:dt:self.time_to_maturity]
        spatial = np.array([-self.spatial_size+i*dz for i in range(self.spatial_partition_size+1)])
        time = np.array([0+i*dt for i in range(self.time_partition_size+1)])


        # Initial conditions and boundary conditions
        for j in range(self.spatial_partition_size+1):
            u[0, j] = np.max([spatial[j], 0])
        u[1:, 0] = 0
        u[1:, -1] = np.max([spatial[j], 0])

        for i in range(1, self.time_partition_size+1):
            # Gamma functions
            gamma_forward = (1 - np.exp(-self.interest_rate * time[i-1])) / (self.interest_rate * self.time_to_maturity)
            gamma_backward = (1 - np.exp(-self.interest_rate * time[i])) / (self.interest_rate * self.time_to_maturity)

            # Argument for matrices
            arg_A_forw = 0.5 * d * (self.volatility**2 / 2) * (gamma_forward - spatial[1:-1])**2
            arg_A_backw = -0.5 * d * (self.volatility**2 / 2) * (gamma_forward - spatial[1:-1])**2


            # Creating matrices and diagonals
            A_forw = np.zeros((self.spatial_partition_size-1, self.spatial_partition_size-1)) + np.diag(1-2*arg_A_forw)
            A_backw = np.zeros((self.spatial_partition_size-1, self.spatial_partition_size-1)) + np.diag(1-2*arg_A_backw)

            # Non-diagonals
            for j in range(self.spatial_partition_size-2):
                A_forw[j+1, j] = arg_A_forw[j+1]
                A_forw[j, j+1] = arg_A_forw[j]

                A_backw[j+1, j] = arg_A_backw[j+1]
                A_backw[j, j+1] = arg_A_backw[j]

            # Boundary vector (arguments but with the last spatial partition element)
            b_forw = np.zeros((self.spatial_partition_size-1))
            b_backw = np.zeros((self.spatial_partition_size-1))
            b_forw[-1] = self.spatial_size * 0.5 * d * (self.volatility**2 / 2) * (gamma_forward - spatial[-1])**2
            b_backw[-1] = -self.spatial_size * 0.5 * d * (self.volatility**2 / 2) * (gamma_backward - spatial[-1])**2

            # Solving
            matrices = np.matmul(u[i-1, 1:-1], np.matmul(np.transpose(np.linalg.inv(A_backw)), np.transpose(A_forw)))
            b_vectors = np.matmul(b_forw.T, np.transpose(np.linalg.inv(A_backw))) - np.matmul(b_backw.T, np.transpose(np.linalg.inv(A_backw)))

            u[i, 1:-1] = matrices + b_vectors

        # Compute spatial value from theorem (Q(0) = 0)
        z_left = 1 / (self.interest_rate * self.time_to_maturity) * (1 - np.exp(-self.interest_rate * self.time_to_maturity))
        z_right = -self.strike_price * np.exp(-self.interest_rate * self.time_to_maturity) / self.initial_price
        z = z_left + z_right

        # Interpolate to find closest possible
        correct_z = 0
        for k in range(self.spatial_partition_size):
            if z >= spatial[k] and z <= spatial[k+1]:
                correct_z = int(np.round((k + (k + 1)) / 2))

        price = self.initial_price * u[-1, correct_z]
        return price


class AsianPutOption(object):
    def __init__(self, initial_price,
                 strike_price,
                 interest_rate,
                 volatility,
                 time_to_maturity: int,
                 time_partition_size: int,
                 spatial_partition_size: int):
        super(AsianPutOption, self).__init__()
        self.initial_price = initial_price
        self.strike_price = strike_price
        self.interest_rate = interest_rate
        self.volatility = volatility
        self.time_to_maturity = time_to_maturity
        self.time_partition_size = time_partition_size
        self.spatial_partition_size = spatial_partition_size

    def solve(self, spatial_size=3):
        self.spatial_size = spatial_size

        dt = self.time_to_maturity / self.time_partition_size
        dz = 2 * (self.spatial_size / self.spatial_partition_size)
        d = dt / dz ** 2

        u = np.zeros((self.time_partition_size+1, self.spatial_partition_size+1))
        #time = np.mslice[0:dt:self.time_to_maturity]
        spatial = np.array([-self.spatial_size+i*dz for i in range(self.spatial_partition_size+1)])
        time = np.array([0+i*dt for i in range(self.time_partition_size+1)])

        # Initial conditions and boundary conditions
        for j in range(self.spatial_partition_size+1):
            u[0, j] = np.max([spatial[j], 0])
        u[1:, 0] = self.spatial_size
        u[1:, -1] = 0

        for i in range(1, self.time_partition_size+1):
            # Gamma functions
            gamma_forward = (1 - np.exp(-self.interest_rate * time[i-1])) / (self.interest_rate * self.time_to_maturity)
            gamma_backward = (1 - np.exp(-self.interest_rate * time[i])) / (self.interest_rate * self.time_to_maturity)

            # Argument for matrices
            arg_A_forw = 0.5 * d * (self.volatility**2 / 2) * (gamma_forward - spatial[1:-1])**2
            arg_A_backw = -0.5 * d * (self.volatility**2 / 2) * (gamma_forward - spatial[1:-1])**2

            # Creating matrices and diagonals
            A_forw = np.zeros((self.spatial_partition_size-1, self.spatial_partition_size-1)) + np.diag(1-2*arg_A_forw)
            A_backw = np.zeros((self.spatial_partition_size-1, self.spatial_partition_size-1)) + np.diag(1-2*arg_A_backw)

            # Non-diagonals
            for j in range(self.spatial_partition_size-2):
                A_forw[j+1, j] = arg_A_forw[j+1]
                A_forw[j, j+1] = arg_A_forw[j]

                A_backw[j+1, j] = arg_A_backw[j+1]
                A_backw[j, j+1] = arg_A_backw[j]

            # Boundary vector (arguments but with the last spatial partition element)
            b_forw = np.zeros((self.spatial_partition_size-1))
            b_backw = np.zeros((self.spatial_partition_size-1))
            b_forw[-1] = self.spatial_size * 0.5 * d * (self.volatility**2 / 2) * (gamma_forward - spatial[-1])**2
            b_backw[-1] = -self.spatial_size * 0.5 * d * (self.volatility**2 / 2) * (gamma_backward - spatial[-1])**2

            # Solving
            matrices = np.matmul(u[i-1, 1:-1], np.matmul(np.transpose(np.linalg.inv(A_backw)), np.transpose(A_forw)))
            b_vectors = np.matmul(b_forw.T, np.transpose(np.linalg.inv(A_backw))) - np.matmul(b_backw.T, np.transpose(np.linalg.inv(A_backw)))
            u[i, 1:-1] = matrices + b_vectors

        # Compute spatial value from theorem (Q(0) = 0)
        z_left = -1 / (self.interest_rate * self.time_to_maturity) * (1 - np.exp(-self.interest_rate * self.time_to_maturity))
        z_right = self.strike_price * np.exp(-self.interest_rate * self.time_to_maturity) / self.initial_price
        z = z_left + z_right

        # Interpolate to find closest possible
        correct_z = 0
        for k in range(self.spatial_partition_size):
            if z >= spatial[k] and z <= spatial[k+1]:
                correct_z = int(np.round((k + (k + 1)) / 2))

        price = self.initial_price * u[-1, correct_z]
        return price