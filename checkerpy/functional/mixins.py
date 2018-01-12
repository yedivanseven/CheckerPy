from typing import Callable
from .composition import CompositionOf


class CompositionClassMixin:
    @classmethod
    def o(cls, other: Callable) -> CompositionOf:
        """Daisy-chain self and other callable into new functional composition.

        Parameters
        ----------
        other: `callable`
            A callable that accepts (i) a single value, (ii) an optional name
            for that value, and (iii) any number of additional keyword
            arguments.

        Returns
        -------
        functional composition: `CompositionOf`
            New functional composition, combining self and the passed argument.

        Raises
        ------
        TypeError
            If the passed argument is not, in fact, a callable.

        """
        return CompositionOf(cls, other)


class CompositionMixin:
    def o(self, other: Callable) -> CompositionOf:
        """Daisy-chain self and other callable into new functional composition.

        Parameters
        ----------
        other: `callable`
            A callable that accepts (i) a single value, (ii) an optional name
            for that value, and (iii) any number of additional keyword
            arguments.

        Returns
        -------
        functional composition: `CompositionOf`
            New functional composition, combining self and the passed argument.

        Raises
        ------
        TypeError
            If the passed argument is not, in fact, a callable.

        """
        return CompositionOf(self, other)
