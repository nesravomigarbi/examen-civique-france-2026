<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/vendor/autoload.php';

use NesraVomigarbi\ExamenCiviqueFrance\Dataset;

function assert_true(bool $condition, string $message): void
{
    if (!$condition) {
        throw new RuntimeException('FAIL: ' . $message);
    }
}

assert_true(count(Dataset::allQuestions()) === 523, 'allQuestions count');
$keys = array_unique(array_column(Dataset::allQuestions(), 'question_key'));
assert_true(count($keys) === 523, 'unique keys');

assert_true(count(Dataset::byMention('CSP')) === 190, 'CSP');
assert_true(count(Dataset::byMention('CR')) === 209, 'CR');
assert_true(count(Dataset::byMention('NAT')) === 258, 'NAT');
assert_true(count(Dataset::byLevel('carte de séjour pluriannuelle')) === 190, 'CSP label');
assert_true(count(Dataset::byMention('naturalisation')) === 258, 'NAT label');

assert_true(count(Dataset::byTheme('T1')) === 93, 'T1');
assert_true(count(Dataset::byTheme('T2')) === 111, 'T2');
assert_true(count(Dataset::byTheme('T3')) === 94, 'T3');
assert_true(count(Dataset::byTheme('T4')) === 143, 'T4');
assert_true(count(Dataset::byTheme('T5')) === 83, 'T5');
assert_true(count(Dataset::byTheme('Histoire, géographie et culture')) === 143, 'T4 name');
$themeTotal = 0;
foreach (array_keys(Dataset::THEMES) as $code) {
    $themeTotal += count(Dataset::byTheme($code));
}
assert_true($themeTotal === 524, 'theme total');

$key = 'Q93946df581';
$inT1 = array_filter(Dataset::byTheme('T1'), static fn (array $q): bool => $q['question_key'] === $key);
$inT3 = array_filter(Dataset::byTheme('T3'), static fn (array $q): bool => $q['question_key'] === $key);
assert_true(count($inT1) === 1 && count($inT3) === 1, 'two-theme question');

$first = Dataset::mockExam(28, ['mention' => 'NAT', 'seed' => 42]);
$second = Dataset::mockExam(28, ['mention' => 'NAT', 'seed' => 42]);
assert_true(count($first) === 28, 'mock exam size');
assert_true(count(array_unique(array_column($first, 'question_key'))) === 28, 'mock exam unique');
assert_true(array_column($first, 'question_key') === array_column($second, 'question_key'), 'seed determinism');
assert_true(count(array_filter($first, static fn (array $q): bool => $q['in_nat'])) === 28, 'all NAT');

$question = Dataset::randomQuestion(['mention' => 'CSP', 'theme' => 'T4', 'seed' => 7]);
assert_true($question['in_csp'] === true, 'random in CSP');
assert_true(in_array('T4', $question['theme_codes'], true), 'random in T4');

$allYears = Dataset::acquisitionsByYear();
assert_true(count($allYears) === 18, '18 years');
assert_true($allYears[0]['year'] === 2008, 'first year');
assert_true($allYears[17]['year'] === 2025, 'last year');
assert_true(Dataset::acquisitionsByYear(2010)['modes']['decree_total']['count'] === 94573, '2010 decree');
assert_true(Dataset::acquisitionsByYear(2025)['modes']['decree_total']['count'] === 42246, '2025 decree');
assert_true(Dataset::acquisitionsByYear(2008)['modes']['declaration_ascendant_sibling']['count'] === null, 'empty 2008 mode');

$threw = false;
try { Dataset::byMention('XYZ'); } catch (InvalidArgumentException $e) { $threw = str_contains($e->getMessage(), 'unknown mention'); }
assert_true($threw, 'unknown mention');
$threw = false;
try { Dataset::byTheme('T9'); } catch (InvalidArgumentException $e) { $threw = str_contains($e->getMessage(), 'unknown theme'); }
assert_true($threw, 'unknown theme');
$threw = false;
try { Dataset::mockExam(0); } catch (InvalidArgumentException $e) { $threw = str_contains($e->getMessage(), 'positive integer'); }
assert_true($threw, 'n=0');
$threw = false;
try { Dataset::mockExam(10000); } catch (InvalidArgumentException $e) { $threw = str_contains($e->getMessage(), 'only 523'); }
assert_true($threw, 'n too large');

echo "All PHP tests passed\n";
