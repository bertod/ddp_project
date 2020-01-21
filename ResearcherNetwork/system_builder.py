# from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from typing import Any
from ResearcherNetwork.scraper import ScraperCreator, ConcreteScraperDblpCreator
from ResearcherNetwork.parser import ParserCreator, ConcreteParserDblpCreator


class AnalyzerBuilder(ABC):
    """
    The Builder interface specifies methods for creating the different parts of
    the Product objects.
    """

    @abstractproperty
    def product(self) -> None:
        pass

    @abstractmethod
    def produce_part_scraper(self, scraper_creator: ScraperCreator) -> None:
        pass

    @abstractmethod
    def produce_part_parser(self, parser_creator: ParserCreator) -> None:
        pass


class SourceAnalyzer:
    """
    This represents the product we want the builder to build
    """

    def __init__(self) -> None:
        self.parts = {}

    def add(self, part: Any, part_name: str) -> None:
        self.parts[part_name] = part

    def list_parts(self) -> None:
        for k, v in self.parts.items():
            print("{} part: OK".format(k))


class Director:
    """
    The Director is responsible for executing the building steps.
    It is helpful when producing products according to a
    specific order/configuration or when you want to keep
    hidden the building steps for a product.
    However, the Director class is optional, since
    the client can control builders directly.
    """

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> AnalyzerBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: AnalyzerBuilder) -> None:
        """
        The Director uses the builder the client code passed to it.
        """
        self._builder = builder

    def build_dblp_analyzer(self) -> None:
        """
        Calling this method, the builder constructs this specific product
        using predefined components
        """
        scraper_creator = ConcreteScraperDblpCreator()
        parser_creator = ConcreteParserDblpCreator()
        self.builder.produce_part_scraper(scraper_creator)
        self.builder.produce_part_parser(parser_creator)


class ConcreteAnalyzerBuilder(AnalyzerBuilder):

    def __init__(self) -> None:
        """
        A fresh builder instance should contain a blank product object, which is
        used in further assembly.
        """
        self.reset()

    def reset(self) -> None:
        self._product = SourceAnalyzer()

    @property
    def product(self) -> SourceAnalyzer:
        product = self._product
        self.reset()
        return product

    def produce_part_scraper(self, scraper_creator: ScraperCreator) -> None:
        self._product.add(scraper_creator, "scraper")

    def produce_part_parser(self, parser_creator: ParserCreator) -> None:
        self._product.add(parser_creator, "parser")
