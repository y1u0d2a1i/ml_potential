import numpy as np


class ElasticTensor:
    """
    Create elastic tensor from C11, C12, C44
    """
    def __init__(self, C11, C12, C44):
        self.C11 = C11
        self.C12 = C12
        self.C44 = C44

    def get_elastic_tensor(self):
        et = np.array(
                [
                    [self.C11, self.C12, self.C12, 0, 0, 0],
                    [self.C12, self.C11, self.C12, 0, 0, 0],
                    [self.C12, self.C12, self.C11, 0, 0, 0],
                    [0, 0, 0, self.C44, 0, 0],
                    [0, 0, 0, 0, self.C44, 0],
                    [0, 0, 0, 0, 0, self.C44],
                ]
            )
        return et


class MechanicalProp:
    def __init__(self, et: np.array):
        """
        Args:
            et: elastic tensor
        """
        self.et = et
        self.c11_cubic = (self.et[0,0] + self.et[1,1] + self.et[2,2]) / 3
        self.c12_cubic = (self.et[0,1] + self.et[1,2] + self.et[2,0]) / 3
        self.c44_cubic = (self.et[3,3] + self.et[4,4] + self.et[5,5]) / 3
        pass

    def get_bulk_modulus(self) -> float:
        """
        definition of bulk modulus is from lammps
        Returns: bulk modulus
        """
        bulk_modulus = (self.c11_cubic + 2 * self.c12_cubic) / 3
        return bulk_modulus

    def get_shear_modulus(self, type: str) -> float:
        """
        Args:
            type: type of definition for shear modulus

            lmp1 -> lammps 1
            lmp2 -> lammps 2
            mp -> material project voigt
        Returns: shear modulus
        """
        if type == 'lmp1':
            return self.c44_cubic
        elif type == 'lmp2':
            return (self.c11_cubic - self.c12_cubic) / 2
        elif type == 'mp':
            return (self.c11_cubic - self.c12_cubic + 3 * self.c44_cubic) / 5
        else:
            raise Exception('invalid type')

    def get_poisson_ratio(self) -> float:
        """
        definition of poisson ratio is from lammps
        Returns: poisson ratio
        """
        poisson_ratio = 1 / (1 + self.c11_cubic / self.c12_cubic)
        return poisson_ratio