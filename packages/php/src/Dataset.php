<?php

declare(strict_types=1);

namespace NesraVomigarbi\ExamenCiviqueFrance;

use InvalidArgumentException;
use RuntimeException;

final class Dataset
{
    public const VERSION = '1.0.0';
    public const DOI = '10.5281/zenodo.24496692';
    public const HOMEPAGE = 'https://examen-civique-test.fr/';

    public const THEMES = [
        'T1' => 'Principes et valeurs de la République',
        'T2' => 'Système institutionnel et politique',
        'T3' => 'Droits et devoirs',
        'T4' => 'Histoire, géographie et culture',
        'T5' => 'Vivre dans la société française',
    ];

    private const MENTION_ALIASES = [
        'csp' => 'CSP',
        'carte de sejour pluriannuelle' => 'CSP',
        'cr' => 'CR',
        'carte de resident' => 'CR',
        'nat' => 'NAT',
        'naturalisation' => 'NAT',
        'naturalization' => 'NAT',
        'nationalite' => 'NAT',
        'nationalite francaise' => 'NAT',
    ];

    private const MENTION_FLAG = [
        'CSP' => 'in_csp',
        'CR' => 'in_cr',
        'NAT' => 'in_nat',
    ];

    /** @var list<array<string, mixed>>|null */
    private static ?array $questions = null;

    /** @var list<array<string, mixed>>|null */
    private static ?array $acquisitions = null;

    private function __construct()
    {
    }

    /**
     * @return list<array<string, mixed>>
     */
    public static function allQuestions(): array
    {
        return self::questions();
    }

    /**
     * @return list<array<string, mixed>>
     */
    public static function byMention(string $mention): array
    {
        $flag = self::MENTION_FLAG[self::normalizeMention($mention)];
        return array_values(array_filter(
            self::questions(),
            static fn (array $question): bool => (bool) $question[$flag]
        ));
    }

    /**
     * @return list<array<string, mixed>>
     */
    public static function byLevel(string $mention): array
    {
        return self::byMention($mention);
    }

    /**
     * @return list<array<string, mixed>>
     */
    public static function byTheme(string $theme): array
    {
        $code = self::normalizeTheme($theme)[0];
        return array_values(array_filter(
            self::questions(),
            static fn (array $question): bool => in_array($code, $question['theme_codes'], true)
        ));
    }

    /**
     * @param array{mention?:string,level?:string,theme?:string,seed?:int|float} $options
     * @return array<string, mixed>
     */
    public static function randomQuestion(array $options = []): array
    {
        $items = self::pool($options);
        if ($items === []) {
            throw new InvalidArgumentException('no questions match the given filters');
        }
        $index = (int) floor(self::randomSource($options['seed'] ?? null)() * count($items));
        return $items[min($index, count($items) - 1)];
    }

    /**
     * @param array{mention?:string,level?:string,theme?:string,seed?:int|float} $options
     * @return list<array<string, mixed>>
     */
    public static function mockExam(int $n, array $options = []): array
    {
        if ($n < 1) {
            throw new InvalidArgumentException('n must be a positive integer');
        }
        $items = self::pool($options);
        if ($n > count($items)) {
            throw new InvalidArgumentException(
                'cannot build a mock exam of ' . $n . ' questions; only ' . count($items) . ' match the filters'
            );
        }
        $random = self::randomSource($options['seed'] ?? null);
        for ($i = 0; $i < $n; $i++) {
            $j = $i + (int) floor($random() * (count($items) - $i));
            $swap = $items[$i];
            $items[$i] = $items[$j];
            $items[$j] = $swap;
        }
        return array_slice($items, 0, $n);
    }

    /**
     * @return list<array<string, mixed>>|array<string, mixed>
     */
    public static function acquisitionsByYear(?int $year = null): array
    {
        if ($year === null) {
            $rows = [];
            foreach (self::acquisitions() as $row) {
                $rows[] = ['year' => $row['year'], 'modes' => $row['modes']];
            }
            return $rows;
        }
        foreach (self::acquisitions() as $row) {
            if ($row['year'] === $year) {
                return ['year' => $row['year'], 'modes' => $row['modes']];
            }
        }
        throw new InvalidArgumentException('no acquisition statistics for year ' . $year);
    }

    public static function normalizeMention(string $mention): string
    {
        if (trim($mention) === '') {
            throw new InvalidArgumentException('mention is required (CSP, CR or NAT)');
        }
        $mapped = self::MENTION_ALIASES[self::fold($mention)] ?? null;
        if ($mapped === null) {
            throw new InvalidArgumentException('unknown mention: ' . $mention . ' (use CSP, CR or NAT)');
        }
        return $mapped;
    }

    /**
     * @return array{0:string,1:string}
     */
    public static function normalizeTheme(string $theme): array
    {
        if (trim($theme) === '') {
            throw new InvalidArgumentException('theme is required (T1–T5 or an official theme name)');
        }
        $key = self::fold($theme);
        foreach (self::THEMES as $code => $name) {
            if ($key === self::fold($code) || $key === self::fold($name)) {
                return [$code, $name];
            }
        }
        throw new InvalidArgumentException('unknown theme: ' . $theme . ' (use T1–T5 or an official theme name)');
    }

    /**
     * @return list<array<string, mixed>>
     */
    private static function questions(): array
    {
        if (self::$questions === null) {
            self::$questions = self::loadJson('questions.json');
        }
        return self::$questions;
    }

    /**
     * @return list<array<string, mixed>>
     */
    private static function acquisitions(): array
    {
        if (self::$acquisitions === null) {
            self::$acquisitions = self::loadJson('acquisitions.json');
        }
        return self::$acquisitions;
    }

    /**
     * @return list<array<string, mixed>>
     */
    private static function loadJson(string $name): array
    {
        $path = dirname(__DIR__) . '/data/' . $name;
        $raw = file_get_contents($path);
        if ($raw === false) {
            throw new RuntimeException('unable to read bundled data file: ' . $name);
        }
        $decoded = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
        if (!is_array($decoded)) {
            throw new RuntimeException('bundled data file is not a JSON array: ' . $name);
        }
        return $decoded;
    }

    private static function fold(string $value): string
    {
        $value = mb_strtolower(trim($value), 'UTF-8');
        $from = ['à','á','â','ä','ã','è','é','ê','ë','ì','í','î','ï','ò','ó','ô','ö','õ','ù','ú','û','ü','ý','ÿ','ç','ñ'];
        $to   = ['a','a','a','a','a','e','e','e','e','i','i','i','i','o','o','o','o','o','u','u','u','u','y','y','c','n'];
        return str_replace($from, $to, $value);
    }

    /**
     * @param array{mention?:string,level?:string,theme?:string,seed?:int|float} $options
     * @return list<array<string, mixed>>
     */
    private static function pool(array $options): array
    {
        $items = self::questions();
        $selected = $options['mention'] ?? $options['level'] ?? null;
        if ($selected !== null) {
            $flag = self::MENTION_FLAG[self::normalizeMention((string) $selected)];
            $items = array_values(array_filter(
                $items,
                static fn (array $question): bool => (bool) $question[$flag]
            ));
        }
        if (isset($options['theme'])) {
            $code = self::normalizeTheme((string) $options['theme'])[0];
            $items = array_values(array_filter(
                $items,
                static fn (array $question): bool => in_array($code, $question['theme_codes'], true)
            ));
        }
        return $items;
    }

    /**
     * @return callable(): float
     */
    private static function randomSource(int|float|null $seed): callable
    {
        if ($seed === null) {
            return static fn (): float => mt_rand() / (mt_getrandmax() + 1);
        }
        $state = ((int) $seed) & 0xFFFFFFFF;
        return static function () use (&$state): float {
            $state = ($state + 0x6D2B79F5) & 0xFFFFFFFF;
            $t = $state;
            $t = (self::imul($t ^ ($t >> 15), $t | 1)) & 0xFFFFFFFF;
            $t = ($t ^ (($t + self::imul($t ^ ($t >> 7), $t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF;
            return (($t ^ ($t >> 14)) & 0xFFFFFFFF) / 4294967296;
        };
    }

    private static function imul(int $a, int $b): int
    {
        return unpack('l', pack('l', ($a * $b) & 0xFFFFFFFF))[1];
    }
}
